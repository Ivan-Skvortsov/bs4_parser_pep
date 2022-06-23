<div id="top"></div>
<div align="center">
<h1>Проект парсинга PEP</h1>
  <h3>
    Парсер документации Python<br />
  </h3>
</div>

## О проекте
Проект представляет собой парсер веб-сайта python.org. В рамках проекта реализовано 4 парсера, предлагающих различный функционал. Функции и режимы работы парсера выбираются через аргументы командной строки.
<p align="right">(<a href="#top">наверх</a>)</p>

## Использованные технологии и пакеты
* [Python](https://www.python.org/)
* [Beautiful Soup](https://beautiful-soup-4.readthedocs.io/en/latest/)
* [Requests Cache](https://requests-cache.readthedocs.io/en/stable/)
<p align="right">(<a href="#top">наверх</a>)</p>

## Необходимый софт
Для запуска проекта потребутеся машина, с предустановленным интерпретатором Python</a>.

## Установка
Склонируйте проект на Ваш компьютер
   ```sh
   git clone https://github.com/Ivan-Skvortsov/bs4_parser_pep.git
   ```
Перейдите в папку с проектом
   ```sh
   cd bs4_parser_pep
   ```
Активируйте виртуальное окружение
   ```sh
   python3 -m venv venv
   ```
   ```sh
   source venv/bin/activate
   ```
Обновите менеджер пакетов (pip)
   ```sh
   pip3 install --upgrade pip
   ```
Установите необходимые зависимости
   ```sh
   pip3 install -r requirements.txt
   ```

## Использование

### Запуск

Запуск парсера осуществляется из командной строки при помощи команды::
   ```sh
   python3 main.py [-h] [-c] [-o {pretty,file}] {whats-new,latest-versions,download,pep}
   ```
### Описание аргументов:


Функции парсера (обязательный аргумент):

    {whats-new,latest-versions,download,pep}

- <b>whats-new</b> - что нового. Будет выполнен парсинг последних новостей с эндпойнта https://docs.python.org/3/whatsnew/. Вывод возможен в терминал и в файл, в зависимости от выбранного режима (см. ниже)
- <b>latest-versions</b> - последние версии. Выполняет парсинг информации о версиях Python. Вывод результата возможен в терминал или файл (см. ниже)
- <b>download</b> - выполняет загрузку архива документации python в формате pdf (A4). Архив загружается в папку /downloads.
- <b>pep</b> - выполняет парсинг эндпойнта https://peps.python.org/. Выводит информацию о статусе pep и их количестве. Вывод результата возможен в терминал и файл.


Режимы работы парсера (опциональный аргумент):

   ```sh
   [-h] [-c] [-o {pretty,file}]
   ```
 - <b>-h</b> - вывод справки
 - <b>-c</b> - запуск программы с очисткой кэша (по умолчанию запросы парсера кэшируются)
 - <b>-o</b> - выбор способа вывода результатов (pretty - вывод в терминал в табличной форме, file - вывод в csv-файл. Файл сохраняется в парке /results). По умолчанию данные выводятся в терминал построчно.


## Об авторе
Автор проекта: Иван Скворцов<br/><br />
[![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Ivan-Skvortsov/)
[![Gmail](https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:pprofcheg@gmail.com)
[![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/Profcheg)
<p align="right">(<a href="#top">наверх</a>)</p>
