### LegendSet
## Установка пакетов: ##

```
sudo apt update
sudo apt install python3 python3-pip gunicorn nginx mc
pip3 install flask
```

## Создаем новую папку и переходим в нее: ##

```
cd ~
mkdir <название проекта>
cd <название проекта>
```

## Клонируем проект с помощью следующей команды: ##

```
git clone https://github.com/vankad24/GameSetServer
```

## Проверяем работу Gunicorn: ##

```
gunicorn --bind 0.0.0.0:8000 run:app
```

# Создаем файл службы `flaskapp.service` с помощью команды `sudo nano /etc/systemd/system/flaskapp.service` и вставляем следующий текст: #

(Замените `имя_пользователя` на ваше имя пользователя.) 
```
[Unit]
Description=flaskapp.service - A Flask application run with Gunicorn.
After=network.target

[Service]
User=имя_пользователя
Group=имя_пользователя
WorkingDirectory=/home/имя_пользователя/<название проекта>
ExecStart=/usr/bin/gunicorn --workers 3 \
--bind unix:/home/имя_пользователя/<название проекта>/flaskapp.sock run:app

[Install]
WantedBy=multi-user.target
```

## Проверяем работу сервиса: ##

```
sudo service flaskapp start
sudo service flaskapp status
```

## Делаем автозагрузку сервиса: ##

```
sudo systemctl enable flaskapp
```

Переходим в директорию `/etc/nginx/` и открываем файл `sudo mc`. В папке `sites-available` создаем копию файла `default`, затем в `sites-enabled` создаем символическую ссылку на этот файл. 

Редактируем содержимое файла следующим образом:
```
location / {
    proxy_pass http://unix:/home/имя_пользователя/<название проекта>/flaskapp.sock;
}
```

Удалите слово `default-server` из строк `listen 80`.

## Проверяем конфигурацию Nginx: ##

```
sudo service nginx configtest
sudo service nginx restart
```

## Теперь вы можете открыть браузер и перейти по вашему серверу. ##

