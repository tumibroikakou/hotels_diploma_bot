# Дипломный проект - Телеграм бот для Too Easy Travel
---


## 1. Введение
Бот выдаёт отели с сайта [Hotels.com](https://hotels.com), отосортированные по
запросу пользователя. Пользователь может работать с ботом через Телеграм.

## 2. Команды

*/lowprice*
 * Отели с сортировкой по цене от низкой к высокой. Пользователь вводит
 название города, количество отелей в ответе и количество картинок в ответе.


*/highprice* 
* Отели с сортировкой по цене от высокой к низкой. Пользователь вводит
название города, количество отелей в ответе и количество картинок в ответе.

*/bestdeal*
* Отели, наиболее подходящие по цене и расположению от центра. Пользователь
вводит максимальное расстояние от центра, вилку цен, название города,
количество отелей в ответе и количество картинок в ответе.


*/settings*
* Настройки бота по умолчанию. Пользователь может поменять дату заезда и
выезда, количество гостей.

*/history*
* История запросов запросов пользователя. Пользователь может просмотреть любой
предыдущий результат.

*/help*
* Как и команда /start, покажет пользователю список доступных команд.

## 3. Запуск
Для запусуа бота в папке с проектом должен находиться файл `.env` такого содержания:

> bot_token = 'ТОКЕН ВАШЕГО БОТА'\
> rapid_api = 'ТОКЕН ВАШЕГО RapidAPI'

Запуск бота выполняется из терминала, из папки с проектом, командой:
`python main.py`

---