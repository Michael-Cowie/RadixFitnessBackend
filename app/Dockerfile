# Use the official Python image as a base image
FROM python:3.9

# Prevents Python from writing pyc files to disc (equivalent to python -B option)
ENV PYTHONDONTWRITEBYTECODE 1

# Prevents Python from buffering stdout and stderr (equivalent to python -u option)
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

COPY . .

EXPOSE 8000

RUN pip install -r requirements.txt

RUN python manage.py collectstatic

# This is executed on container startup, the RUN instructions are used on image creation.
CMD ["gunicorn", "backend.wsgi:application", "--bind", "0.0.0.0:8000"]
