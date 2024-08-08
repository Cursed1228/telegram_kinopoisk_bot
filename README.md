# Проект Telegram-бота для поиска фильмов и сериалов
Этот проект представляет собой Telegram-бота, который позволяет пользователям искать фильмы и сериалы по различным критериям,
таким как бюджет, рейтинг, жанр и название, а так же просматривать историю запросов. Бот использует API для получения информации о фильмах и сериалов и хранит историю
поиска пользователей в базе данных.

# Основные функции
1. Поиск фильмов с низким бюджетом
Команда: /low_budget_movie
Описание: Позволяет пользователю выбрать жанр и количество результатов для поиска фильмов с низким бюджетом.
2. Поиск фильмов по рейтингу
Команда: /movie_by_rating
Описание: Позволяет пользователю ввести рейтинг и жанр для поиска фильмов по рейтингу.
3. Поиск фильмов по названию
Команда: /movie_search
Описание: Позволяет пользователю ввести название фильма или сериала и количество результатов для поиска.
4. Поиск фильмов с высоким бюджетом
Команда: /high_budget_movie
Описание: Позволяет пользователю выбрать жанр и количество результатов для поиска фильмов с высоким бюджетом.
5. Просмотр истории поиска
Команда: /history
Описание: Позволяет просмотреть все фильмы или сериалы которые искал пользователь, а также отметить если они просмотрены

# Установка
1. Установите все библиотеки из файла "requirements.txt"
2. Получить токен бота.
Для этого перейдите к отцу ботов [BotFather](https://t.me/BotFather)  и нажмите на START или «ЗАПУСТИТЬ».
В появившемся сообщении со списком команд выберите /newbot.
![Alt text](image.png)

Выберите имя для бота. При необходимости это имя можно будет потом изменить.
Задайте боту username — это уникальное имя, которое уже нельзя будет изменить. Оно обязательно должно оканчиваться на слово bot.
После выбора имени вы получите токен бота, необходимый для дальнейшей работы.

![Alt text](image-1.png)
3. Получение API токена.
Перейдите по [ссылке](https://kinopoisk.dev/)
Нажмите "Получить доступ к API".
Дальше следуйте инструкциям telegram бота.
4. Создание .env
Для корректной работы вам нужно создать файл ".env" по аналогии с ".env.template", заменить строки на ваши ключи.
5. БД
Создать файл базы данных, для сохранения в неё истории просмотров и внести название файла в ".env"
Например: "Moving_database.db"
