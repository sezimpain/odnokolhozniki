from django.core.mail import send_mail
from odnokolhozniki.celery import app


@app.task
def notify_user(email):
    send_mail('Вы опубликовали новый пост!',
              'Спасибо за использование нашего сайта',
              'odnokolhozniki@admin.com',
              [email]
              )
    return 'Success'