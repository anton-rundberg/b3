from b3.celery import app

from . import models


@app.task
def send_reset_password_email(user_pk):
    user = models.User.objects.get(pk=user_pk)
    user.send_password_reset_email()
