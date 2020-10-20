# DMonitor

[![](https://img.shields.io/badge/%D0%A7%D0%B0%D1%82%D1%8B%20%D0%9C%D0%93%D0%A3-%40chat__msu-blue)](https://t.me/chat_msu/22333)

[![](https://img.shields.io/badge/%D0%93%D1%80%D0%B0%D1%84%D0%B8%D0%BA%D0%B8%20|%20%D0%93%D0%97%20%D0%B8%20%D0%94%D0%A1%D0%9B-internet.msut.me-9cf)](https://internet.msut.me)
[![](https://img.shields.io/badge/%D0%93%D1%80%D0%B0%D1%84%D0%B8%D0%BA%D0%B8%20|%20%D0%94%D0%90%D0%A1-internet.msut.me/das-7cf)](https://internet.msut.me/das)

[![](https://img.shields.io/badge/%D0%9F%D1%80%D0%B8%D1%81%D0%BE%D0%B5%D0%B4%D0%B8%D0%BD%D0%B8%D1%82%D1%8C%D1%81%D1%8F-internet.msut.me%2Fjoin-brightgreen)](https://internet.msut.me/das)

## Программа для мониторинга интернета в общежитиях МГУ

> ![](https://i.imgur.com/8fSJOVs.jpg)


## Зачем
- интернет в общежитиях МГУ должен быть лучше
- собираемая статистика поможет понять проблемы

## Как присоединиться
Каждый житель Главного здания, ДСЛ и ДАС может помочь общему делу.

Для этого нужно всего лишь запустить программу `DMonitor` и держать её открытой.

Скачать `DMonitor` можно в разделе [релизы](https://github.com/uburuntu/dmonitor/releases/latest).

## Про DMonitor

Схема работы:
- программа работает в фоновом режиме и раз в минуту проверяет доступ к `google.com`, `yandex.ru` и `vk.com`
- если доступ есть, то на `StatHat` отправляется среднее время ответа сайтов
- если интернет отключился, то программа сохраняет на диск информацию об этом и отправляет эти логи при первой возможности

Программа ест около 10-30 МБ оперативной памяти и не делает ничего больше, не требует установки и не засоряет систему.

## Обратная связь

Чаты общежитий:
- Главное здание: [@ds_msu](https://t.me/ds_msu)
- ДСЛ: [@dsl_msu](https://t.me/dsl_msu)
- ДАС: [@das_msu](https://t.me/das_msu)

Будем рады обратной связи:
- если возникают какие-то проблемы, то сообщайте
- если есть идеи и предложения, то не стесняйтесь предлагать и обсуждать

## Графики

https://internet.msut.me

## Скачать

https://github.com/uburuntu/dmonitor/releases/latest

### Настроить автозапуск

Для запуска программы при перезагрузке системы можно воспользоваться [скриптами](https://github.com/uburuntu/dmonitor/autorun_scripts) (потребуются администраторские права). 

#### Windows

- Запустите `dmonitor_autorun.bat` от имени администратора
- Введите путь к `DMonitorWin.exe`

#### Linux

- Запустите `dmonitor_autorun.sh`
- Введите путь к `DMonitorLinux`

#### MacOS

- Запустите `dmonitor_autorun.bash`
- Введите путь к `DMonitorMacOS.zip`
