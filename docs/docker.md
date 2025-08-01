<div align="center">
 <h1> Docker for Development </h1>
</div>

The `docker-compose.yaml` is responsible for setting up the PostgreSQL database, connecting our DRF application to the 
database and starting up the Nginx server to be hosted on port `1337`. When executing the docker compose for the
first time, there are some necessary steps to configure the database. Keep in mind this only needs to be done once,
per volume because the volume will have correctly configured the database setting which will be mounted to each
new container. This is found at,

```YAML
  db:
    image: postgres:16
    volumes:
      - postgres_data:/var/lib/postgresql/data/
  ...
```

### 1. Change to the correct directory
The base directory is `backend` but the necessary development files are located inside of `app`. Therefore, change to 
the `app` directory by running `cd app`.

### 2. Start up the Containers

Docker compose is responsible for the initialization of all the necessary containers located inside the 
`docker-compose.yaml` file. The command for execute Docker compose is `docker compose up`.

### 3. Initialize the Database

The initial state of our PostgreSQL database does not contain our user created tables. This can be visible by using
the follows commands,

First, from within the `db` container, run the `psql` executable with the following commands.

```commandline
docker compose exec db psql --username=admin --dbname=radix_fitness_postgresql_db
```

This command allows us to execute PostgresSQL commands through a CLI by connecting to the `radix_fitness_postgresql_db`
database logged in as admin. When connected we can see that there are currently no tables present in the database, shown
below.

![](./images/psql_no_relations.png)

In order to initialize the user tables, we need to run the following command,

```commandline
docker compose exec web python manage.py migrate
```

This command will be executed within the `web` container and tells Django to run all the migrations files located
in each app migrations folder. Running it for the first time will also create the tables.

![](./images/apply_migration.png)

Now, after running this command we can refresh the database and see the created tables.

![](./images/after_migration.png)

### 4. Create a superuser in order to use the adminstration page.

The next step is to create a superuser. This is required to authenticate to the admin page, which should now
be visible at `localhost:1337/admin`. To create a superuser, run the following command,

```commandline
docker compose exec web python manage.py createsuperuser
```

Using the newly created superuser account, we can authenticate and seeing the administration page. Because this is
a fresh volume, their will be no user data.

### Additional development information

Each newly created images do not need to reinitialize the commands above. As long as they're mounted to the same
volume where the instructions were ran. This is shown by the database service,

```YAML
  db:
    image: postgres:16
    volumes:
      - postgres_data:/var/lib/postgresql/data/
```

Keep in mind, volume mounting only occurs during run-time and not build-time, i.e. for containers and not for images.
The same applies, new containers do not need to rerun these instructions as it will be mounted to the folder where
these instructions have already occurred, this is the same location where the PostgreSQL data is stored. Therefore,
only rerun the instructions for each new volume.