FROM python:3.9
LABEL MAINTAINER=" smrtsilver | srtongsnoop@gmail.com"

ENV PYTHONUNBUFFERED 1

# Set working directory
RUN mkdir /collage
WORKDIR /collage
COPY . /collage

# Installing requirements
ADD requirements/requirements.txt /collage
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Collect static files
RUN python manage.py collectstatic --no-input

CMD ["gunicorn", "--chdir", "collage", "--bind", ":8000", "collage.wsgi:application"]
