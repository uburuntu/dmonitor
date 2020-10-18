---
layout: page
title: Присоединиться
---

## Зачем это всё
- интернет в общежитиях МГУ должен быть лучше
- собираемая статистика поможет понять проблемы

## Как присоединиться
Каждый житель Главного здания и ДСЛ может помочь общему делу.

Для этого нужно всего лишь запустить программу `DMonitor` и держать её открытой.

Скачать `DMonitor` можно на [GitHub](https://github.com/uburuntu/dmonitor/releases/latest).

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

Будем рады обратной связи:
- если возникают какие-то проблемы, то сообщайте
- если есть идеи и предложения, то не стесняйтесь предлагать и обсуждать

## Исходный код

Доступен на [GitHub](https://github.com/uburuntu/dmonitor).