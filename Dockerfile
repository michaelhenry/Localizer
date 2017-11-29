FROM python:3.6.3
MAINTAINER Michael Henry Pantaleon

ENV PROJECT_PATH /home
WORKDIR $PROJECT_PATH

COPY requirements.txt $PROJECT_PATH
RUN pip install -r requirements.txt
COPY . $PROJECT_PATH

ENV DJANGO_SETTINGS_MODULE LocalizrExample.settings.production
ENV PORT 8001

EXPOSE $PORT
RUN chmod +x deploy.sh
ENTRYPOINT sh deploy.sh