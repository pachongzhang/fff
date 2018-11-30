import sys
import os
import django

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

sys.path.append(r'C:\Users\admin\Desktop\moviespider\movieweb')
os.environ['DJANGO_SETTINGS_MODULE'] = 'movieweb.settings'
django.setup()

