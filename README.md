# Start the Server

Run the command,

```
python manage.py runserver
```

Ideally, have this configured in PyCharm.

Now’s a good time to note, don’t use this server in anything resembling a production environment. 
It’s intended only for use while developing. (Django is in the business of making web frameworks, not web servers.)

# Model Changes

When Models have been altered, you need to migrate the database. Then this is done from the following command,

```console
python manage.py makemigrations
python manage.py migrate
```

The server will need to be restarted after running these two commands.

# Architecture

Django is used as a backend, therefore we will primarily be using the [django-rest-framework](https://www.django-rest-framework.org/tutorial/quickstart/)
library to create a RESTful API, we will not be utilizing Django to return any HTML.

# Authorzation

As of now, we use Firebase for our account creation and management. The user is expected to send us a JWT(JSON Web Token)
when sending a request to our backend. To handle all requests and verify that the token prior to forwarding it
to our Views, I have created a Middleware class called `FirebaseTokenMiddleware`. This Middleware is responsible
for checking the authenticity of the token, parse it and then forward the user UID to our Views.