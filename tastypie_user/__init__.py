"""
A RESTful APIs for User resource, base on Tastypie.
"""
__author__ = 'hepochen'

from django.contrib.auth import get_user_model

User = get_user_model()

print User
