# Автоподнятие резюме на Headhunter
Позволяет автоматически поднимать первое (самое верхнее) резюме на Headhunter.<br>

### Необходимо:
- ОС семейства Unix
- python3
- почта на mail.ru
- разрешение доступа внешним приложениям на email (app password)
- создать папку `hh_codes` в вашем email и настроить фильтр (входящие сообщения сохранятся в этой папке) для сообщений имеющих адрес `noreply@hh.ru` и тему сообщения `Код подтверждения`
- Минимум 1GB RAM
- Файл `.env` 
    ```text
    USER_EMAIL=your@mail.ru
    USER_PASSWORD=your_APP_password_in_email
    EMAIL_SERVER=imap.mail.ru
    ```

## Запуск
### На компьютере:
Предполагается что вы разрешили доступ внешним приложениям на email и получили пароль для приложения, а так же создали папку `hh_codes` на email и настроили фильтры.<br>
#### Выполняем последовательно команды
```commandline
mkdir raise_resume && cd raise_resume/
```
```commandline
git clone https://github.com/NankuF/headhunter_raise_resume.git
```
```commandline
cd headhunter_raise_resume/
```
```commandline
nano .env
```
```commandline
# в .env вставляем
USER_EMAIL=your@mail.ru
USER_PASSWORD=your_APP_password_in_email
```
```commandline
python3 -m venv venv
```
```commandline
. ./venv/bin/activate
```
```commandline
pip install -r requirements.txt
```
```commandline
python3 main.py
```
### В докере (на компьютере или на сервере)
Вы скачали репозиторий и успешно запустили на компьютере/сервере. Теперь создайте образ и запустите в докере.
```commandline
docker build . -t hh_raise_resume
```
```commandline
docker run -d --restart unless-stopped --name hh_raise_resume -v $(pwd)/logs:/app/logs -e TZ=$(cat /etc/timezone) --env-file .env -v /dev/shm:/dev/shm hh_raise_resume
```
Другой вариант нагуглите сами: создать образ на локальном компьютере, запушить его в свой докер-репозиторий, и затем на сервере запустить приложение в контейнере, спуллив его с докер-репозитория.

### Известные проблемы
_Программа виснет на слабых серверах (500мб RAM) даже с пробросом /dev/shm в контейнер._<br>
Пробросить /dev/shm тк google chrome не хватает памяти в контейнере
[link](https://stackoverflow.com/questions/53902507/unknown-error-session-deleted-because-of-page-crash-from-unknown-error-cannot)
```commandline
docker run --name <your_name_container> --env-file .env -v /dev/shm:/dev/shm <your_image>

```
