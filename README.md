# API Manager

This is a Django project to manage the Open Bank Project API via API Calls.

To use this app, you need to authenticate against a sandbox where you have to have registered an account beforehand. Currently, you can enable or disable consumers.


# Installation (development)

It is assumed that the git checkout resides inside a project directory, e.g. inside `/var/www/apimanager` and thus to be found at `/var/www/apimanager/API-Manager`.
Paths below are relative to this README. Files produced during installation or at runtime should be outside the git checkout, but inside the project directory, except for Django's local settings. 
The directory tree might look like:

```bash
/var/www/apimanager/
├── API-Manager
│   ├── apimanager
│   ├── apimanager.service 
│   ├── gunicorn.conf.py
│   ├── LICENSE
│   ├── nginx.apimanager.conf
│   ├── NOTICE
│   ├── README.md
│   ├── requirements.txt
│   └── supervisor.apimanager.conf
├── db.sqlite3
├── logs
├── static-collected
└── venv
```

## Install dependencies

```bash
$ virtualenv --python=python3 ../venv
$ source ../venv/bin/activate
(venv)$ pip install -r requirements.txt
```
Note: if this fails you may be missing the `python3-tk` and `tk` packages:

```bash 
$ sudo apt install python3-tk tk
```

## Configure settings

Create and edit `apimanager/apimanager/local_settings.py`:

```python
import os
BASE_DIR = '/your/base/dir'
EXCLUDE_APPS = []
EXCLUDE_FUNCTIONS = []
EXCLUDE_URL_PATTERN = []
API_EXPLORER_APP_NAME = 'API Explorer app name'
API_DATEFORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'
# Used internally by Django, can be anything of your choice
SECRET_KEY = '<random string>'
# API hostname, e.g. https://api.openbankproject.com
API_HOST = '<hostname>'
# Consumer key + secret to authenticate the _app_ against the API
OAUTH_CONSUMER_KEY = '<key>'
OAUTH_CONSUMER_SECRET = '<secret>'
# Database filename, default is `../db.sqlite3` relative to this file
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, '..', '..', 'db.sqlite3'),
    }
}
```

Changes to this file will not be overwritten on updates. The settings there can override anything specified in `apimanager/apimanager/settings.py`.

The application's authentication is API-driven. However, to make use of Django's authentication framework and sessions, there is a minimal requirement of a database. Per default, sqlite is used, but you can configure any Django-supported backend you want. Please lookup the appropriate documentation.


## Initialise database

```bash
(venv)$ ./apimanager/manage.py migrate
```

## Run the app

```bash
(venv)$ ./apimanager/manage.py runserver
```

The application should be available at `http://localhost:8000`


# Installation (production)

Execute the same steps as for development, but do not run the app.

## Settings

Edit `apimanager/apimanager/local_settings.py` for _additional_ changes to the development settings above:

```python

import os
# Disable debug
DEBUG = False
# Hosts allowed to access the app
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '<your public hostname here>']

# Directory to place static files in, defaults to `../static-collected` relative to this file
STATIC_ROOT = ''
# Admins to send e.g. error emails to
ADMINS = [
        ('Admin', 'admin@example.com')
]
# Emails are sent from this address
SERVER_EMAIL = 'apimanager@example.com'
# Emails are sent to this host
EMAIL_HOST = 'mail.example.com'
# Enable email security
EMAIL_TLS = True

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Used internally by Django, can be anything of your choice
SECRET_KEY = 'abc'
# API hostname, e.g. https://api.openbankproject.com
API_HOST = 'http://127.0.0.1:8080'
# Consumer key + secret to authenticate the _app_ against the API
OAUTH_CONSUMER_KEY = ''
OAUTH_CONSUMER_SECRET = ''
# Database filename, default is `../db.sqlite3` relative to this file
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, '..', '..', 'db.sqlite3'),
    }
}

# Apps to exclude when request to OBP-API's api
EXCLUDE_APPS = []
# Functions to exclude when request to OBP-API's api
EXCLUDE_FUNCTIONS = []
# Url Patterns to exclude when reqeust to OBP-API's api
EXCLUDE_URL_PATTERN = []

# App Name to aggregate metrics  
API_EXPLORER_APP_NAME = 'xxx'

#Map Java: yyyy-MM-dd'T'HH:mm'Z'
API_DATETIMEFORMAT = '%Y-%m-%dT%H:%M:%SZ'
#Map Java: yyyy-MM-dd'T'HH:mm:ss.SSS'Z'
API_DATEFORMAT = '%Y-%m-%dT%H:%M:%S.000Z'

```

## Static files

The app's static files, e.g. Javascript, CSS and images need to be collected and made available to a webserver. Run

```bash
(venv)$ ./apimanager/manage.py collectstatic
```

The output will show where they are collected to (`settings.STATIC_ROOT`).

## Web application server

Instead of Django's built-in runserver, you need a proper web application server to run the app, e.g. `gunicorn`. It should have been installed already as a dependency and you can use the provided `gunicorn.conf.py`. Run it like

```bash
(venv)$ cd apimanager/ && gunicorn --config ../gunicorn.conf.py apimanager.wsgi 
```

- `gunicorn` does not start successfully when omitting the directory change and using `apimanager.apimanager.wsgi` as program.
- The user running  `gunicorn` needs to have write access to the _directory_ containing the database, as well as the database file itself.
- The app's output is logged to `gunicorn`'s error logfile (see `gunicorn.conf.py` for location)


## Process control

If you do not want to start the web application server manually, but automatically at boot and also want to restart automatically if it dies, a process control system comes in handy. This package provides configuration files for systemd and supervisor.

### systemd

Stick the provided file `apimanager.service` into `/etc/systemd/system/`, edit to suit your installation and start the application (probably as root):

```bash
# /bin/systemctl start apimanager
```

If it works properly, you might want it to be started at boot:

```bash
# /bin/systemctl enable apimanager
```

If you need to edit the service file afterwards, it needs to be reloaded as well as the service
```bash
# /bin/systemctl daemon-reload
# /bin/systemctl restart apimanager
```


### supervisor

Stick the provided file `supervisor.apimanager.conf` into `/etc/supervisor/conf.d/`, edit to suit your installation and restart supervisor (probably as root):

```bash
# /bin/systemctl restart supervisor
```

## Webserver

Finally, use a webserver like `nginx` or `apache` as a frontend. It serves static files from the directory where `collectstatic` puts them and acts as a reverse proxy for gunicorn. Stick the provided `nginx.apimanager.conf` into `/etc/nginx/sites-enabled/`, edit it and reload the webserver (probably as root):

```bash
# /bin/systemctl reload nginx
```


# Management

The app should tell you if your logged in user does not have the proper role to execute the management functionality you need. Please use a Super Admin user to login and set roles at `/users` to rectify that. To become Super Admin, set the property `super_admin_user_ids` in the API properties file accordingly.


# Final words

Be aware of file permission issues and preconfigured paths to executables (system env versus virtual env)!

Have fun,
 TESOBE
