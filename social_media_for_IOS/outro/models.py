from django.db import models

# Create your models here.


class User(models.Model):
    mail = models.EmailField()
    password = models.TextField()
    name = models.TextField()
    role = models.TextField()
    picture = models.FileField()


class Mark(models.Model):
    user = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
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
    user = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
    task = models.ForeignKey('Task', on_delete=models.SET_NULL, null=True)
    file = models.FileField()


class Chat(models.Model):
    name = models.TextField()


class ChatMembers(models.Model):
    user = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
    chat = models.ForeignKey('Chat', on_delete=models.SET_NULL, null=True)


class Message(models.Model):
    text = models.TextField()
    date = models.DateTimeField()
    user = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
    chat = models.ForeignKey('Chat', on_delete=models.SET_NULL, null=True)


class ChatAttache(models.Model):
    file = models.FileField()
    message = models.ForeignKey('Message', on_delete=models.SET_NULL, null=True)


class LastRead(models.Model):
    user = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
    chat = models.ForeignKey('Chat', on_delete=models.SET_NULL, null=True)
    message = models.ForeignKey('Message', on_delete=models.SET_NULL, null=True)
