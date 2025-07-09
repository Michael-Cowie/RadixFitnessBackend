<div align="center">
    <h1> Project Architecture </h1>
</div>

Starting a new project requires the command,

```console
django-admin startproject backend
```

This command generates a skeletal framework with crucial configurations. The main files are,

```
backend/                 <-- Generated
├── manage.py
├── backend/
│   ├── __init__.py
│   ├── asgi.py
│   ├─ settings.py
│   ├─ urls.py
│   ├── wsgi.py
```

However, this is already done and only needed to be executed once. This is the project, and is under the directory
called `backend` in our environment.

- **manage.py -** Contains various Django management commands. It's the tool through which you initiate
 the development server, create applications, run migrations, and more.
- **backend/settings.py -** Contains the settings that configure your project, from database configurations to 
 middleware lists. This is where you define how your application functions.
- **backend/urls.py -** The URL dispatcher, encoded within `urls.py` maps URLs to Views. This file determines which 
 view is displayed when a specific URL is accessed.
- **backend/wsgi.py -** Short for Web Server Gateway Interface, `wsgi.py` serves as the entry point for your application when deployed
 on a production server. It's the bridge connecting your application to the web server, enabling it to handle incoming requests.
- **backend/asgi.py -** Similar to `wsgi.py`, `asgi.py` is the entry point for asynchronous web servers. It stands for  Asynchronous
 Server Gateway Interface and facilitates the handling of asynchronous HTTP requests.

For each project, there are many applications. The main project here is `backend` and will not require anymore
to be created. Contribution to the project will require creation of new `apps`. Here, A `project` refers to the entire application and all its parts. An `app` refers to a submodule of the project. It's self-sufficient and not intertwined with the other `apps` in the project such that, in theory, you could pick it up and plop it down into another project without any modification. An app typically has its own `models.py` (which might actually be empty). You might think of it as a standalone python module. A simple project might only have one app.

We create a new `app` with the following command,

```
python manage.py startapp <my_app>
```

The two commands will generate,

```
my_project/
├── manage.py
├── my_project/
│   ├── __init__.py
│   ├── asgi.py
│   ├─ settings.py
│   ├─ urls.py
│   ├── wsgi.py
├── my_app/                 <-- Generated
    ├── migrations/
    │   └── __init__.py
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── models.py
    ├── tests.py
    ├── urls.py
    └── views.py
```

The follows files generated,

- **models.py -** At the heart of every application lies the `models.py` file. This is where you define the data structures using Djangos ORM (Object-Relational Mapping). Each model class represents a table in the database. This file forms the foundation of your application's data management.
- **views.py -** The `views.py` file encapsulates the logic that defines how your application interacts with user's requests. Views handle data processing, rendering templates and responding to actions. This file transforms user interactions into tangible responses.
- **tests.py -** Test-driven development gains momentum through the `tests.py` file. Here, you write unit tests to ensure your application's components function as expected.
- **admin.py -** The `admin.py` file isn't just for administrators - it configures how your application's models are
 presented in Djangos admin interface. This file allows administrators to manage data seamlessly.
- **migrations -** This directory is a blueprint of all changes in your application models.
- **Other files -** Additional files might surface based on your applicants needs. For example, `forms.py` houses form classes for data input, `urls.py` maps URLs to Views. `apps.py` manages application-specific configurations. `serializers.py` serves the purpose of transforming the database data into a datatype that javascript can use.

Creating a new `app` will require it to be added to the projects `INSTALLED_APPS`,

```Python
INSTALLED_APPS = [
    'my_app',
    ...
]
```

The `django-rest-framework` introduces a new file called `serializers.py`, this is not added by default when creating a new `app`. The first thing we need to get started on our Web API is to provide a way of serializing and deserializing the `app` instances into representations such as `json`. We can do this by declaring serializers that work very similar to Django's forms. A serializer is what determines that information that is being sent back for each request.