# API Manager

A Django project to manage the Open Bank Project API via API Calls


## Installation (development)

Paths are relative to this README.

### Install dependencies

```bash
$ virtualenv --python=python3 venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

### Configure settings

Edit `apimanager/apimanager/local_settings.py`:

```python
SECRET_KEY = '<random string>'
OAUTH_API = '<your API root, e.g. https://api.openbankproject.com>'
OAUTH_CLIENT_KEY = 'key you got from the API'
OAUTH_CLIENT_SECRET = 'secret you got from the API'
DATABASES['default']['NAME'] = '<Filename to use for database>' # default is 'db.sqlite3' in parent directory of git checkout
```

The application's authentication is API-driven. However, to make use of Django's authentication framework and sessions, there is a minimal requirement of a database. Per default, sqlite is used, but you can configure any Django-supported backend you want. Please lookup the appropriate documentation.


### Initialise database

```bash
$ ./apimanager/manage.py migrate
```


### Run the app

```bash
$ ./apimanager/manage.py runserver
```

The application should be available at `http://localhost:8000`


## Installation (production)

Execute the same steps as for development, but do not run the app.

### Settings

Edit `apimanager/apimanager/local_settings.py` for additional changes:

```python
DEBUG = False
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '<your hostname here>']
STATIC_ROOT = '<Directory to place static files in>'
```

### Static files

The app's static files, e.g. Javasript, CSS and images need to be collected and made available to a webserver. Run

```bash
$ ./apimanager/manage.py collectstatic
```

### Web application server

Instead of Django's built-in runserver, you need a proper web application server to run the app, e.g. `gunicorn`. It should have been installed already as a dependency and you use the provided `gunicorn.conf.py`. Run it like

```bash
$ cd apimanager/ && gunicorn --config ../gunicorn.conf.py apimanager.wsgi 
```

For some reason, the process does not start successfully when omitting the directory change and using `apimanager.apimanager.wsgi` as program.

### Process control

If you do not want to start the web application server manually, but automatically at boot and also want to restart automatically if it dies, a process control system like `supervisor` comes in handy. Stick the provided file `supervisor.apimanager.conf` into `/etc/supervisor/conf.d/`, edit it and reload supervisor (probably as root):

```bash
# /bin/systemctl restart supervisor
```

### Webserver

Finally, use a webserver like `nginx` or `apache` as a frontend. It serves static files from the directory where `collectstatic` puts them and acts as a reverse proxy for gunicorn. Stick the provided `nginx.apimanager.conf` into `/etc/nginx/sites-enabled/`, edit it and reload the webserver (probably as root):

```bash
# /bin/systemctl reload nginx
```


## Final words

As usual, be aware of file permission issues!

Have fun,
 TESOBE
