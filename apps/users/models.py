from __future__ import unicode_literals

from django.db import models

import datetime

import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')

class QuoteManager(models.Manager):
    def validation(self, requestPost):
        string = ""
        if len(requestPost['quotedby']) < 3:
            string += "| Name is too short |"
        if len(requestPost['message']) < 10: 
            string += "| Quote is too short |"
        return string

class UserManager(models.Manager):
    def validation(self, requestPost):
        string = ""
        if User.objects.filter(email=requestPost['email']):
            string += "| Email already exists |"
        if len(requestPost['name']) < 1:
            string += "| Please enter a name |"
        if len(requestPost['alias']) < 1: 
            string += "| Please enter an alias |"
        if re.match(NAME_REGEX, requestPost['name']) == None:
            string += "| Name may only contain letters |"
        if re.match(EMAIL_REGEX, requestPost['email']) == None:
            string += "| Invalid E-mail |"
        if requestPost['password'] != requestPost['confirm_password']:
            string += "| Password does not match confirm password |"
        if len(requestPost['password']) < 8:
            string += "| Password should be at least 8 characters |"
        if len(requestPost['dob']) < 8:
            string += "| Please enter your date of birth |"
        else:
            compare_time_start = datetime.datetime.strptime(requestPost['dob'], '%Y-%m-%d') - datetime.datetime.today()
            if compare_time_start.total_seconds() > 0:
                string += "| Please enter a valid date of birth |"
        return string

class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    dob = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Quote(models.Model):
    message = models.CharField(max_length=10000)
    quotedby = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name = "quotes")
    favoritedby = models.ManyToManyField(User)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = QuoteManager()