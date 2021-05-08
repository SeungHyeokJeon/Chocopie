# Capstone Project

### Requirement
- django
- mysqlclient
### Installation and Run Sever

```bash
$ pip insatll django==3.2
$ pip install mysqlclient
```

```bash
../Chocopie/ $ python manage.py makemigrations
../Chocopie/ $ python manage.py migrate
```

```bash
# run server
../Chocopie/ $ python manage.py runserver
```

### 필독사항

- settings.py에 들어간 비밀키와 db정보는 Notion/Django/Secrets 항목 확인할 것