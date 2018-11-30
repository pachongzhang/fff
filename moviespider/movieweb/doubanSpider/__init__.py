# coding;utf-8
# def setup_django_env():
#     import os, django, sys
#     sys.path.append('/home/rock/Desktop/moviespider/movieweb')
#
#     os.environ.setdefault("DJANGO_SETTINGS_MODULE", "movieweb.settings")
#     django.setup()
#
# def check_db_connection():
#     from django.db import connection
#
#     if connection.connection:
#         #NOTE: (zacky, 2016.MAR.21st) IF CONNECTION IS CLOSED BY BACKEND, CLOSE IT AT DJANGO, WHICH WILL BE SETUP AFTERWARDS.
#         if not connection.is_usable():
#             connection.close()
