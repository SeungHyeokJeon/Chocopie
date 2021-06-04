# Capstone Project

### Requirement
- django
- mysqlclient
### Installation and Run Sever

```bash
$ pip install django==3.2
$ pip install mysqlclient
$ pip install django-allauth
$ pip install pillow
$ pip install django-summernote
```
- 실행 전 Notion/Django/Secrets에 있는 Secrets.json파일을 받아 최상위 폴더에 저장
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
