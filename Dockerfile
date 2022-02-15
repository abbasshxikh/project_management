FROM python:3.7
ENV PYTHONUNBUFFERED 1
RUN mkdir /app
WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r requirements.txt
# RUN apt-get install sudo
# RUN sudo apt-get install redis-server
# RUN python manage.py migrate
COPY . /app/


# FROM python:3.7

# ENV PYTHONUNBUFFERED 1

# COPY ./requirements.txt /requirements.txt
# RUN pip install -r /requirements.txt

# RUN mkdir /app
# WORKDIR /app

# COPY ./app /app