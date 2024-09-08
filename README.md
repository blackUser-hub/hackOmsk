# ELIZAR
Telegram Bot нa python, выполняющий функцию ИИ-секретаря.

Для запуска склонируйте репозиторий в каталог, не имеющий в своем названии русских букв
```
git clone https://github.com/blackUser-hub/hackOmsk.git
```

# На компьютерах с ОС Windows:
Скачайте приложение [Docker Desktop](https://www.docker.com/products/docker-desktop/) и проведите его первоначальную настройку

В каталоге программы выполните команду:
```
docker compose up -d
```
# На компьютерах с Linux:
Перейдите на [сайт документации docker](https://docs.docker.com/engine/install/), выберите свою систему и следуйте инструкциям

В каталоге программы выполните команду:
```
docker compose up -d
```


# Взаимодействие с СУБД

Перейдите в админ панель базы данных по [ссылке](localhost:15432) и войдите по данным из файла .env (PGADMIN_EMAIL, PGADMIN_PASSWORD)

  1. На главном экране нажмите "Add new server"
  2. Во вкладке General введите postgres в поле "name"
  3. Во вкладке Connection введите db в поле "Host name", username и password из .env (DB_USER, DB_PASSWORD)
  4. Нажмите "connect"

Перейдите в бота по [ссылке](https://t.me/aisecretary52bot) и наслаждайтесь работой

