from django.db import models
from django.contrib.auth.models import User


class CustomUser(User):
    role = models.TextField(choices=[('Student', 'student'), ('Assistant', 'assistant'),
                                     ('Teacher', 'teacher')])
    picture = models.FileField()
    accepted = models.BooleanField(default=False)


class Mark(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.SET_NULL, null=True)
    date = models.DateField()
    mark = models.IntegerField()
    weight = models.FloatField()


class Task(models.Model):
    name = models.TextField()
    text = models.TextField()
    start = models.DateTimeField()
    finish = models.DateTimeField()


class TaskAttache(models.Model):
    file = models.FileField()
    task = models.ForeignKey('Task', on_delete=models.SET_NULL, null=True)


class Answer(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.SET_NULL, null=True)
    task = models.ForeignKey('Task', on_delete=models.SET_NULL, null=True)
    file = models.FileField()


class Chat(models.Model):
    name = models.TextField()


class ChatMembers(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.SET_NULL, null=True)
    chat = models.ForeignKey('Chat', on_delete=models.SET_NULL, null=True)


class Message(models.Model):
    text = models.TextField()
    date = models.DateTimeField()
    user = models.ForeignKey('CustomUser', on_delete=models.SET_NULL, null=True)
    chat = models.ForeignKey('Chat', on_delete=models.SET_NULL, null=True)


class ChatAttache(models.Model):
    file = models.FileField()
    message = models.ForeignKey('Message', on_delete=models.SET_NULL, null=True)


class LastRead(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.SET_NULL, null=True)
    chat = models.ForeignKey('Chat', on_delete=models.SET_NULL, null=True)
    message = models.ForeignKey('Message', on_delete=models.SET_NULL, null=True)
