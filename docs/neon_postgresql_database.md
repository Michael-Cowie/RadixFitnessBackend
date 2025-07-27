<div align="center">
    <h1> Neon Database Integration with Django Backend </h1>
</div>

Neon is a fully managed, cloud-native PostgreSQL database service. It is built with a focus on serverless operations, automatic scaling and developer productivity. In the Radix Fitness backend, which is implemented using the Django web framework, Neon serves as the primary relational database, handling persistent storage for the user data, fitness goals, tracking records and more. Django communicates with Neon using a PostgreSQL-compatible connection via the standard `psycopg2` or `psycopg2-binary` database driver. The database connection is configured using a single `DATABASE_URL` environment variable.

Neon makes it extremely simple to provision new PostgreSQL database via its web dashboard or CLI. Once an account is created,

1. You can provision a new project, which corresponds to a Neon-managed PostgreSQL instance.
2. Each project can have multiple branches (like Git) and each branch can have one or more databases.
3. Typically, a `main` branch is used for production and `dev` or `preview` branch is used for development and staging environment.

Each database comes with a unique PostgreSQL connection string that can be copied directly from the Neon dashboard. You will find it under `Connect to your database` box.

<div align="center">
    <img src="./images/neon_branches.png">
</div>

## Connecting via PostgreSQL URL

A PostgreSQL connection to Neon is expressed using a URL of the following form.

```
postgresql://<username>:<password>@<host>/<database>?<options>
```

An example URL could be,

```perl
postgresql://neondb_owner:npg_m4jaRhWu5YSQ@ep-little-band-z12345bc-pooler.ap-southeast-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require
```

- `postgresql://` - Specifies the protocol and driver.
- `neondb_owner` - The username.
- `npg_m4jaRhWu5YSQ` - The password.
- `ep-little-band-z12345bc-pooler.ap-southeast-2.aws.neon.tech` - The host.
- `neondb` - Database name.
- `?sslmode=require` - Ensures SSL/TLS is used for encrypted connections.
- `&channel_binding=require` - Enforces TLS channel binding for extra security, this is required by Neon.

Django supports database configuration through environment variables using the popular `dj-database-url` utility. To configure Django to connect to Neon, the `DATABASE_URL` environment variable must be set. This is environment variable will be set within the web-service which runs Django, as of now it is `fly.io`.

The current database configuration is setup to prioritize using the `DATABASE_URL` but has the fallback setup to use SQLite for local test execution.

```ini
DATABASE_URL=postgresql://neondb_owner:npg_m4jaRhWu5YSQ@ep-little-band-z12345bc-pooler.ap-southeast-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require
```

By default, `dj_database_url.config()` will search for the `DATABASE_URL` environment variable and return a configured dictionary for Django, otherwise return `None` which will cause the code to fallback and use the environment variables configured in the `default.ini` file.

```python
# If DATABASE_URL is set, use it. Otherwise, use defaults.ini
DATABASES = {
    "default": dj_database_url.config()
    or {
        ...
    }
}
```

## Database Connection Using Neon Web UI and DBeaver

#### Neon Web UI

Suppose we take the `Profile` model as an example.

```python
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    name = models.CharField(max_length=100, validators=[alpha])
    measurement_system = models.CharField(choices=Units.choices, max_length=8)

    def __str__(self):
        return self.name
```

Neon displays the table in a friendly UI where it has 4 columns.

- `user_id` - This is the primary key and a foreign key to `auth_user.id` from the `User` Model.
- `name` - The users profile name. 
- `measurement_system` - The user selected measurement system.
- `auth_user` - This is an implicit reference to the related `auth_user` table used for joins in the UI. The `auth_user` column you see is a foreign key link shown by the Neon UI, not a separate database column. It just displays the related table name (`auth_user`) for reference.

<div align="center">
    <img src="./images/neon_table_web_ui.png">
</div>

#### DBeaver

Instead of using the Neon Web UI we can connect directly using DBeaver with the `DATABASE_URL` string. Given the previously mentioned `DATABASE_URL` DBeaver needs the following properties.

- `Host` - `ep-little-band-z12345bc-pooler.ap-southeast-2.aws.neon.tech`
- `Port` - `5432` by default.
- `Databse` - `neondb`
- `Username` - `neondb_owner`
- `Password` - `npg_m4jaRhWu5YSQ`

<div align="center">
    <img src="images/dbeaver_login.png">
</div>

This will show the previously visible profile row as follows.

<div align="center">
    <img src="images/dbeaver_database_profile.png">
</div>

