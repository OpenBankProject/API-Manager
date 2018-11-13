FROM python:3.7.1
RUN apt update && apt install -y dumb-init nginx
RUN pip install -U pip
RUN pip install virtualenv
RUN virtualenv /.venv
RUN mkdir /static
COPY . /src
WORKDIR /src
RUN bash -c 'source /.venv/bin/activate && pip install -r requirements.txt'
RUN mkdir /etc/apimanager
COPY ./sample.local_settings.py /etc/apimanager/local_settings.py
VOLUME /etc/apimanager
RUN echo 'daemon off;' >> /etc/nginx/nginx.conf
RUN ln -sf /etc/apimanager/local_settings.py apimanager/apimanager/local_settings.py
RUN ln -sf /etc/apimanager/nginx.conf /etc/nginx/sites-enabled/api-manager
RUN rm -f /etc/nginx/sites-enabled/default
RUN bash -c 'source /.venv/bin/activate && ./apimanager/manage.py collectstatic'
CMD dumb-init ./start.sh
