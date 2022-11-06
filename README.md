# webcrawler
Software Academy 2022 - course project

# За сайта:
https://nauka.offnews.bg/ е сайт за новини от науката и технологиите, въпроси и теми от областта на природните науки и критичното мислене. 

# Задача:
Да се извлекат статии от последните 90 дни от всички категории на сайта.

Данните, които трябва да се съхранят в база данни (MySQL или MongoDB) са:
- Категория
- Заглавие
- Дата
- Текст

Да се състави потребителски интерфейс в който да се представят таблично получените данни.

Трябва да има поле за филтриране по заглавие и възможност за сортиране (в намаляващ/увеличаващ ред) по дата.

# Забележка:
Crawler-а трябва да се съобразява с правилата в https://nauka.offnews.bg/robots.txt

# Configuration
Create a config.ini file in the root directory including the following configurations:

    [mysql]
    HOST = 
    USER = 
    PASSWORD = 
    DATABASE =
    PORT = 

# Requirements
    pip install -r requirements.txt
