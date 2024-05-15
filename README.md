## О проекте
Проект создан для автоматизации поиска нужных вещей на куфаре с интеграцией в Telegram

### Для создания вебхука, телеграму нужен url на https, поэтому нам нужен ngrock для туннелирования порта нашего веб-сервера 

Установка ngrok на Linux

```commandline
curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null && echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list && sudo apt update && sudo apt install ngrok
```
Установка ngrok на Windows: https://ngrok.com/download

Авторизация ngrok

```commandline
ngrok config add-authtoken 2g34CrRxtp576yu8TjXL3zMnhk5_EtHZf4pigEVvTkTCLVpc
```

Начать туннелирование указанного порта
```commandline
ngrok http 8000
```

>**Далее необходимо внести Forwarding-адрес в .env в переменную NGROK_URL=адрес**

Получения телеграм-токена:
Необходимо в @botfather создать бота, получить его токен.

>**Далее нужно внести его .env в переменную TG_TOKEN=токен**

Установка пакетов:

```commandline
pip install -r requirements.txt
```

### Создание БД
PostgreSQL
```commandline
docker run --name some-postgres -e POSTGRES_PASSWORD=mysecretpassword -p 5432:5432 -d postgres
```
* `--name some-postgres`: Дает имя контейнеру `some-postgres`.
* `-e POSTGRES_PASSWORD=mysecretpassword`: Устанавливает пароль для пользователя postgres.
* `-p 5432:5432`: Пробрасывает порт 5432 из контейнера на хост-машину.
* `-d postgres`: Запускает контейнер в фоновом режиме и использует образ `postgres` из Docker Hub.

>**Далее необходимо внести в .env следующие переменные:**
```
POSTGRES_PASSWORD=
POSTGRES_USER=
POSTGRES_DB=
POSTGRES_PORT=
POSTGRES_HOST=
```


### Инициализация БД и миграции
1. Создание файла миграции
```commandline
alembic revision --autogenerate -m "Database creation"
```
2. Применение миграций
```commandline
alembic upgrade head
```

### Запуск Redis:
```commandline
docker run -p 6379:6379 -d redis:5
```
### Запуск приложения
```commandline
python src/main.py
```