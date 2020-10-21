import logging
import sys
import traceback

from throttler import ExecutionTimer

import config
from pinger import Pinger
from stathat import StatHat
from utils import Timer, CheckMyIP, SingleInstance

logging.basicConfig(format='[%(asctime)s] [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)


def close(status: int):
    input('Нажмите Enter, чтобы закрыть программу: ')
    sys.exit(status)


def main():
    s = SingleInstance()
    if not s.try_lock():
        logging.critical('Одновременно может быть запущена только одна версия программы')
        return close(1)

    et = ExecutionTimer(60.)
    stathat = StatHat(config.stathat_key)
    pinger = Pinger(stathat)
    ip_checker = CheckMyIP()

    try:
        pinger.ping()
    except PermissionError:
        return logging.critical('Нет доступа к сокетам, есть два варианта:\n'
                                '— запускайте программу с sudo\n'
                                '— единоразово дайте разрешение программе ловить пакеты: '
                                'sudo setcap cap_net_raw+ep ./DMonitor-Console-Linux')

    if ip_checker.get_ip() is None:
        logging.critical('Первый запуск программы должен быть при работающем интернете')
        return close(2)

    timer_notify_lost = Timer(30 * 60.)
    timer_notify_net = Timer(30 * 60.)

    logging.info('Мониторинг интернета запущен. Спасибо за участие!')

    try:
        while True:
            with et:
                if provider := ip_checker.provider():
                    ok = pinger.analyze(provider)
                    if ok:
                        timer_notify_lost.reset()
                    else:
                        if timer_notify_lost.acquire():
                            logging.warning(f'Проблема с доступом к одному из сайтов: {", ".join(config.domains)}. '
                                            f'Информация об этом сохранена на диск и будет отправлена при первой возможности.')

                    timer_notify_net.reset()
                else:
                    if timer_notify_net.acquire():
                        logging.warning('Кажется, вы подключены не к сети МГУ. '
                                        'Выгрузка статистики приостановлена до переподключения к ней.')

    except (KeyboardInterrupt, SystemExit):
        logging.info('Bye!')
        sys.exit(0)
    except Exception as e:
        logging.error(f'\nException: {repr(e)}\n\nTraceback: {traceback.format_exc()}\n\nYou can send this logs to t.me/rm_bk, thanks.')
        return close(3)


if __name__ == '__main__':
    main()
