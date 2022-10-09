# Автоподнятие резюме на Headhunter
Позволяет автоматически поднимать первое (самое верхнее) резюме на Headhunter.

### Необходимо:
- ОС семейства Unix
- python3
- разрешение доступа внешним приложениям на email (app password)
- создать папку `hh_codes` в вашем email и настроить фильтр (входящие сообщения сохранятся в этой папке) для сообщений имеющих адрес `noreply@hh.ru` и тему сообщения `Код подтверждения`
- Минимум 1GB RAM
- Файл `.env` 
    ```text
    USER_EMAIL=your@mail.ru
    USER_PASSWORD=your_APP_password_in_email
    ```

## Запуск
### На компьютере:

### В докере (на компьютере или на сервере)
```commandline
docker run -d --restart always --name hh_raise_resume -v $(pwd)/logs:/app/logs -e TZ=$(cat /etc/timezone) --env-file .env -v /dev/shm:/dev/shm   nanku/hh_raise_resume
```

### Известные проблемы
_Программа виснет на слабых серверах (500мб RAM) даже с пробросом /dev/shm в контейнер._<br>
Пробросить /dev/shm тк google chrome не хватает памяти в контейнере
[link](https://stackoverflow.com/questions/53902507/unknown-error-session-deleted-because-of-page-crash-from-unknown-error-cannot)
```commandline
docker run --name <your_name_container> --env-file .env -v /dev/shm:/dev/shm <your_image>

```
