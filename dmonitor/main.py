import time

import PySimpleGUIWx as sg

import config

from pinger import Pinger
from stathat import StatHat
from utils import Timer


def main():
    updates_interval = 60.
    timer = Timer(updates_interval).start()
    timer_notification = Timer(30 * 60.)
    stathat = StatHat(config.stathat_key)
    pinger = Pinger(stathat)

    menu = ['UNUSED', ['Информация', '---', 'Закрыть']]
    last_send = 'Данные еще не отправлялись'
    tooltip = 'Мониторинг интернета в общежитии ГЗ'
    tray = sg.SystemTray(menu=menu, tooltip=f'{tooltip}\n\n{last_send}', data_base64=config.icon)

    while True:
        event = tray.read(timeout=updates_interval * 1000)

        if event == 'Закрыть':
            break

        if timer.acquire():
            ok = pinger.analyze()
            if ok:
                last_send = f'Последняя отправка данных: {time.ctime()}'
                tray.update(tooltip=f'{tooltip}\n\n{last_send}')
            else:
                if timer_notification.acquire():
                    sg.popup_no_wait(f'Проблема с доступом к одному из сайтов: {", ".join(config.domains)}', icon=config.icon)

        if event == 'Информация':
            sg.popup_no_wait(f'{config.text_about}\n\n{last_send}', icon=config.icon)

    tray.close()


if __name__ == '__main__':
    main()
