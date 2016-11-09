#!/usr/bin/env python
import multiprocessing
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

bind = '127.0.0.1:8000'
accesslog = os.path.join(BASE_DIR, 'logs', 'gunicorn.access.log')
errorlog = os.path.join(BASE_DIR, 'logs', 'gunicorn.error.log')
loglevel = 'info'
capture_output = True
workers = multiprocessing.cpu_count() * 2 + 1
