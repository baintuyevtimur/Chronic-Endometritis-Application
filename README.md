# Chronic Endometritis Application

Веб-калькулятор на Django с моделью машинного обучения (XGBoost).  
После запуска приложение доступно по пути `/chronic-endometritis-app/`.

---

## Структура проекта

```
Chronic-Endometritis-Application-main/
│   manage.py
│   requirements.txt
│   gunicorn.service        # Пример unit-файла — используйте как ориентир
│   nginx.conf              # Пример конфига Nginx — используйте как ориентир
│
├── chronic_endometritis_app/
│   ├── ml_models/
│   │   └── m5.json         # Файл модели XGBoost
│   ├── services/
│   ├── templates/
│   └── ...
├── core/                   # Настройки Django (settings.py, wsgi.py и др.)
├── staticfiles/            # Статика уже собрана, collectstatic не нужен
└── requirements.txt
```

---

## Системные требования

- **ОС:** Linux (Ubuntu/Debian)
- **Python:** 3.12
- **Nginx** (установлен и настроен на сервере)
- **Библиотека libgomp1** — обязательна для работы XGBoost:

```bash
sudo apt update
sudo apt install -y libgomp1
```

---

## Развёртывание

### 1. Распаковать архив

```bash
unzip Chronic-Endometritis-Application-main.zip -d /path/to/project
cd /path/to/project/Chronic-Endometritis-Application-main
```

### 2. Создать и активировать виртуальное окружение

```bash
python3.12 -m venv venv
source venv/bin/activate
```

### 3. Установить зависимости

```bash
pip install -r requirements.txt
```

> Если при запуске XGBoost возникает ошибка, связанная с `libgomp`, убедитесь, что пакет `libgomp1` установлен (см. раздел «Системные требования»).

---

## Конфигурация Gunicorn

**WSGI-модуль:** `core.wsgi:application`

Приложение работает через **Unix-сокет** (см. пример `gunicorn.service`).  
Пример запуска для проверки:

```bash
gunicorn core.wsgi:application \
    --workers 3 \
    --bind unix:/var/www/Chronic-Endometritis-Application-main/app.sock
```

В файле `gunicorn.service` в корне проекта находится **пример** systemd unit-файла.  
На его основе создайте `/etc/systemd/system/gunicorn_chronic.service`, подставив:

- путь к директории проекта (`WorkingDirectory`)
- путь к gunicorn внутри виртуального окружения (`ExecStart`)
- путь к сокет-файлу (`app.sock`)
- пользователя, от имени которого будет работать сервис

После создания unit-файла:

```bash
sudo systemctl daemon-reload
sudo systemctl enable gunicorn_chronic
sudo systemctl start gunicorn_chronic
```

---

## Конфигурация Nginx

> **Важно:** на сервере уже работают другие приложения с теми же `server_name`.  
> Не создавайте новый `server`-блок — добавьте блоки `location` в **существующий** конфиг для `dev.sbamsr.irk.ru` / `84.237.24.66`.

В файле `nginx.conf` в корне проекта находится **пример** конфигурации.

Ключевые блоки для добавления в существующий `server`-блок:

**Приложение** — только `/chronic_endometritis_app/`, не `/` (иначе сломаются другие приложения):
```nginx
location /chronic_endometritis_app {
    include proxy_params;
    proxy_pass http://unix:/path/to/Chronic-Endometritis-Application-main/app.sock;
}
```

**Статика** (`collectstatic` запускать не нужно, файлы уже в `staticfiles/`):
```nginx
location /static/ {
    alias /path/to/Chronic-Endometritis-Application-main/staticfiles/;
}
```

После изменения конфига:

```bash
sudo nginx -t
sudo systemctl reload nginx
```

---

## Параметры Django (справочно)

| Параметр | Значение |
|---|---|
| `WSGI_APPLICATION` | `core.wsgi.application` |
| `SETTINGS_MODULE` | `core.settings` |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `localhost`, `127.0.0.1`, `dev.sbamsr.irk.ru`, `84.237.24.66` |
| Статика | `staticfiles/` (уже собрана) |
| База данных | Не используется, миграции не нужны |
| ML-модель | `chronic_endometritis_app/ml_models/m5.json` |

> `SECRET_KEY` задан напрямую в `core/settings.py`. Менять не нужно.

---

## Проверка работоспособности

После запуска Gunicorn и Nginx откройте в браузере:

```
http://84.237.24.66/chronic_endometritis_app/
```

или

```
http://dev.sbamsr.irk.ru/chronic_endometritis_app/
```

---

## Возможные проблемы

| Проблема | Решение |
|---|---|
| `ImportError: libgomp.so.1` при старте | `sudo apt install -y libgomp1` |
| Статика не отдаётся (CSS/JS) | Проверьте путь `alias` к папке `staticfiles/` в конфиге Nginx |
| `502 Bad Gateway` | Проверьте, запущен ли Gunicorn: `sudo systemctl status gunicorn_chronic` |
| `DisallowedHost` в логах | Убедитесь, что IP/домен сервера есть в `ALLOWED_HOSTS` в `core/settings.py` |
| Сломались другие приложения на сервере | Убедитесь, что добавили `location /chronic_endometritis_app`, а не `location /` |
