FROM python:3.10
USER root
COPY . /app
COPY .github/local_settings_container.py /app/apimanager/apimanager/local_settings.py
COPY .github/gunicorn.conf.py /app/gunicorn.conf.py
RUN pip install -r /app/requirements.txt
WORKDIR /app
RUN ./apimanager/manage.py migrate
RUN chgrp -R 0 /app && chmod -R g+rwX /app
USER 501
WORKDIR /app/apimanager
EXPOSE 8000
CMD ["gunicorn", "--bind", ":8000", "--config", "../gunicorn.conf.py", "apimanager.wsgi"]