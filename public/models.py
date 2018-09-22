# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    A = '3+ days'
    B = '2 days'
    C = 'Today'
    D = 'Yesterday'
    E = '2+ days ago'
    EXPIRATION = ((A, '3+ days'), (B, '2 days'), (C, 'Today'), (D, 'Yesterday'), (E, '2+ days ago'))
    expires = models.CharField(max_length=5, choices=EXPIRATION)

class Provider(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    A = '18-29'
    B = '30-39'
    C = '40-49'
    D = '50-59'
    E = '60-69'
    F = '70+'
    AGE_CHOICES = ((A, '18-29'), (B, '30-39'), (C, '40-49'), (D, '50-59'), (E, '60-69'), (F, '70+'))
    age = models.CharField(max_length=5, choices=AGE_CHOICES)
