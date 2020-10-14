import time

import PySimpleGUIWx as sg

import config
from pinger import Pinger
from stathat import StatHat
from utils import Timer, CheckMyIP


def main():
    timer = Timer(1 * 60.).start()
    stathat = StatHat(config.stathat_key)
    pinger = Pinger(stathat)
    ip_checker = CheckMyIP()

    if ip_checker.get_ip() is None:
        return sg.popup_ok('Первый запуск программы должен быть при работающем интернете', icon=config.icon)

    timer_notification_1 = Timer(30 * 60.)
    timer_notification_2 = Timer(30 * 60.)

    menu = ['UNUSED', ['Информация', '---', 'Закрыть']]
    last_send = 'Данные еще не отправлялись'
    tooltip = 'Мониторинг интернета в общежитии ГЗ'
    tray = sg.SystemTray(menu=menu, tooltip=f'{tooltip}\n\n{last_send}', data_base64=config.icon)

    sg.popup_no_wait('Мониторинг интернета запущен, выгрузка статистики начнётся через 1 минуту.\n\n'
                     'Это окно можно закрыть, я продолжу работать в фоновом режиме.\n\n'
                     'Спасибо за участие!', icon=config.icon)

    while True:
        event = tray.read(timeout=1000)

        if timer.acquire():
            if ip_checker.check():
                ok = pinger.analyze()
                if ok:
                    last_send = f'Последняя отправка данных: {time.ctime()}'
                    tray.update(tooltip=f'{tooltip}\n\n{last_send}')
                else:
                    if timer_notification_1.acquire():
                        sg.popup_no_wait(f'Проблема с доступом к одному из сайтов: {", ".join(config.domains)}', icon=config.icon)
            else:
                if timer_notification_2.acquire():
                    sg.popup_no_wait('Кажется, вы подключены не к сети Главного здания.\n\n'
                                     'Выгрузка статистики приостановлена до переподключения к ней.', icon=config.icon)

        if event == 'Закрыть':
            break

        if event == 'Информация':
            sg.popup_no_wait(f'{config.text_about}\n\n{last_send}', icon=config.icon)

    tray.close()


if __name__ == '__main__':
    main()
