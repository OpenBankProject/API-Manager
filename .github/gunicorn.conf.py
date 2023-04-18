#!/usr/bin/env python
import multiprocessing
import os


bind = '127.0.0.1:8000'
accesslog = '-'
errorlog = '-'
loglevel = os.getenv('DEBUG_LEVEL', 'info')
workers = multiprocessing.cpu_count() * 2 + 1
