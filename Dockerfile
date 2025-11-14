FROM python:3.10

# Create non-root user
RUN groupadd --gid 1000 appuser \
    && useradd --uid 1000 --gid appuser --shell /bin/bash --create-home appuser

COPY requirements.txt /app/
COPY apimanager/ /app/apimanager/
COPY static/ /app/static/
COPY gunicorn.conf.py /app/gunicorn.conf.py
COPY .github/local_settings_container.py /app/apimanager/apimanager/local_settings.py
RUN pip install -r /app/requirements.txt
WORKDIR /app
RUN ./apimanager/manage.py migrate

# Set proper ownership and switch to non-root user
RUN chown -R appuser:appuser /app
USER appuser

WORKDIR /app/apimanager
EXPOSE 8000
CMD ["gunicorn", "--bind", ":8000", "--config", "../gunicorn.conf.py", "apimanager.wsgi"]