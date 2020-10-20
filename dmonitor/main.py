import time
import traceback

import PySimpleGUIWx as sg

import config
from pinger import Pinger
from stathat import StatHat
from utils import Timer, CheckMyIP, SingleInstance


def popup(text: str, blocking: bool = False, copiable: bool = False):
    text = sg.MultilineOutput(text, size=(550, 300)) if copiable else sg.Text(text)
    button = sg.Button if blocking else sg.DummyButton

    window = sg.Window(
        'DMonitor',
        [[text], [button('OK')]],
        element_justification='right', resizable=False, icon=config.icon
    )

    if blocking:
        event, values = window.read()
        window.Close()
        return event

    event, values = window.read(timeout=0)
    return event, values


def main():
    sg.theme('DarkAmber')

    s = SingleInstance()
    if not s.try_lock():
        return popup('Одновременно может быть запущена только одна версия программы', blocking=True)

    timer = Timer(1 * 60.).start()
    stathat = StatHat(config.stathat_key)
    pinger = Pinger(stathat)
    ip_checker = CheckMyIP()

    try:
        pinger.ping()
    except PermissionError:
        return popup('Нет доступа к сокетам, есть два варианта:\n'
                     '— запускайте программу с sudo\n'
                     '— дать разрешение программе ловить пакеты: sudo setcap cap_net_raw+ep ./DMonitor-Linux',
                     copiable=True, blocking=True)

    if ip_checker.get_ip() is None:
        return popup('Первый запуск программы должен быть при работающем интернете', blocking=True)

    timer_notify_lost = Timer(60 * 60.)
    timer_notify_net = Timer(60 * 60.)

    menu = ['UNUSED', ['Информация', '---', 'Закрыть']]
    last_send = 'Данные еще не отправлялись'
    tooltip = 'Мониторинг интернета в общежитиях МГУ'
    tray = sg.SystemTray(menu=menu, tooltip=f'{tooltip}\n\n{last_send}', data_base64=config.icon)
    tray.show_message('Мониторинг интернета запущен', 'Выгрузка статистики начнётся через 1 минуту.\n\nСпасибо за участие!', time=3000)

    try:
        while True:
            event = tray.read(timeout=1000)

            if timer.acquire():
                if provider := ip_checker.provider():
                    ok = pinger.analyze(provider)
                    if ok:
                        last_send = f'Последняя отправка данных: {time.ctime()}'
                        tray.update(tooltip=f'{tooltip}\n\n{last_send}')

                        timer_notify_lost.reset()
                    else:
                        if timer_notify_lost.acquire():
                            tray.show_message('Потерян доступ в интернет',
                                              'Информация об этом сохранена и будет отправлена при первой возможности.')

                    timer_notify_net.reset()
                else:
                    if timer_notify_net.acquire():
                        tray.show_message('Текущее подключение не в сети МГУ',
                                          'Выгрузка статистики приостановлена до переподключения к ней.')

            if event == 'Закрыть':
                break

            if event == 'Информация':
                popup(f'{config.text_about}\n\n{last_send}.', copiable=True)

    except Exception as e:
        popup(f'Exception: {repr(e)}\n\nTraceback: {traceback.format_exc()}\n\n'
              f'You can send this logs to t.me/rm_bk, thanks.', copiable=True, blocking=True)
    finally:
        tray.close()


if __name__ == '__main__':
    main()
