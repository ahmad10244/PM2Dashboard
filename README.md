# PM2 Admin Dashboard

## Description

Open-source **Flask Dashboard** for monitoring and managing [PM2](https://pm2.io/) processes.

This Dashboard use [pm2-dashrest](https://github.com/ahmad10244/pm2-dashrest) as a middlewre to connect to pm2 instance.\
Install [pm2-dashrest](https://github.com/ahmad10244/pm2-dashrest) on every server that you want to monitor and manage \
after that add server in `Manage Servers` page

![Login Page!](/static/images/dashboard/login.png)
![Home Page!](/static/images/dashboard/home.png)
![Manage Servers Page!](/static/images/dashboard/manage_server.png)
![Server process Page!](/static/images/dashboard/server.png)

## Docker

Dashboard app can be started with docker.

> ### **Step 1** - Download the code from the GitHub repository (using `GIT`)

``` bash
git clone https://github.com/ahmad10244/PM2Dashboard && cd PM2Dashboard
```

> ### **Step 2** - Create a new `.env` file using sample `env.sample`

Docker will create a postgresql container (from `Postgresql setting` in `.env` file) \
and connect Dashboard app to postgresql container with `SQLALCHEMY_DATABASE_URI` in `.env` file.

- `WEB_PORT`: Port to access Dashboard.
- `PG_PORT`: Postgresql port that use to check if postgresql container started completely.
- `SECRET_KEY`: Random string with symbols, digits, chars, ... to use for flask SECRET_KEY
- `SQLALCHEMY_DATABASE_URI`: Postgresql URI for using in app db connections. \
    format: `postgresql://username:password@host:port/database`
- `POSTGRES_USER`: Username that used for creating postgresql container.
- `POSTGRES_PASSWORD`: Password that used for creating postgresql container.
- `POSTGRES_DB`: DataBase name that used for creating postgresql container.
- `TZ`: TimeZone that used for creating postgresql container.
- `PGTZ`: TimeZone that used for creating postgresql container.

> ### **Step 3** - Start the Dashboard in Docker

``` bash
docker-compose up --build
```

Visit `http://localhost:{WEB_PORT}` in your browser. The app should be up & running.\
(default: `http://localhost:8080`)

## Contributing

> ### **Step 1**

Install python3.9+, pip3, virtualenv, Postgresql in your system

> ### **Step 2** - Clone source code from the GitHub repository and setup virtualenv

``` bash
git clone https://github.com/ahmad10244/PM2Dashboard && cd PM2Dashboard
virtualenv -p python3 venv
source venv/bin/activate
```

> ### **Step 3** - Install requirements

:warning: Requires python3.9+

``` bash
pip install -r requirements.txt
```

> ### **Step 4** - Set configs and upgrade database tables

``` bash
export FLASK_DEBUG=1
export SQLALCHEMY_DATABASE_URI=postgresql://username:password@host:port/database
export SECRET_KEY='random string with symbols, digits, chars, ...'
flask db upgrade
```

> ### **Step 5** - Run in development mode

``` bash
flask run
```

Visit `http://localhost:5000` in your browser. The app should be up & running.
