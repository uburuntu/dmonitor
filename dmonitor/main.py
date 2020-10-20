import time
import traceback

import PySimpleGUIWx as sg

import config
from pinger import Pinger
from stathat import StatHat
from utils import Timer, CheckMyIP


def popup(text: str, blocking: bool = False, copiable: bool = False):
    text = sg.MultilineOutput(text, size=(500, 300)) if copiable else sg.Text(text)
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

    timer = Timer(1 * 60.).start()
    stathat = StatHat(config.stathat_key)
    pinger = Pinger(stathat)
    ip_checker = CheckMyIP()

    if ip_checker.get_ip() is None:
        return popup('Первый запуск программы должен быть при работающем интернете', blocking=True)

    timer_notification_1 = Timer(60 * 60.)
    timer_notification_2 = Timer(60 * 60.)

    menu = ['UNUSED', ['Информация', '---', 'Закрыть']]
    last_send = 'Данные еще не отправлялись'
    tooltip = 'Мониторинг интернета в общежитиях МГУ'
    tray = sg.SystemTray(menu=menu, tooltip=f'{tooltip}\n\n{last_send}.', data_base64=config.icon)

    popup('Мониторинг интернета запущен, выгрузка статистики начнётся через 1 минуту.\n\n'
          'Это окно можно закрыть, я продолжу работать в фоновом режиме.\n\n'
          'Спасибо за участие!')

    try:
        while True:
            event = tray.read(timeout=1000)

            if timer.acquire():
                if provider := ip_checker.provider():
                    ok = pinger.analyze(provider)
                    if ok:
                        last_send = f'Последняя отправка данных: {time.ctime()}'
                        tray.update(tooltip=f'{tooltip}\n\n{last_send}')
                    else:
                        if timer_notification_1.acquire():
                            popup(f'Проблема с доступом к одному из сайтов: {", ".join(config.domains)}.\n\n'
                                  f'Информация об этом сохранена на диск и будет отправлена при первой возможности.')
                else:
                    if timer_notification_2.acquire():
                        popup('Кажется, вы подключены не к сети МГУ.\n\nВыгрузка статистики приостановлена до переподключения к ней.')

            if event == 'Закрыть':
                break

            if event == 'Информация':
                popup(f'{config.text_about}\n\n{last_send}.', copiable=True)

    except Exception as e:
        popup(f'Exception: {repr(e)}\n\nTraceback: {traceback.format_exc()}', blocking=True)
    finally:
        tray.close()


if __name__ == '__main__':
    main()
