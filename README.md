# Faculty Portal

## Getting Started

Clone or fork the repo to make changes and test the site.

### Prerequisites

Install django and PostgreSQL.


### Installing

Create a vitual enviroment if you have to deal with multiple python projects.

```
sudo apt-get install python-virtualenv
or
sudo easy_install virtualenv
or
sudo pip3 install virtualenv
```

```
mkdir ~/virtualenvironment
virtualenv ~/virtualenvironment/my_new_app
cd ~/virtualenvironment/my_new_app/bin
source activate
```

To install the requirements
Note: Use sudo only if some errors pop up.

```
pip install -r requirements.txt
```

Follow [these instructions](https://www.digitalocean.com/community/tutorials/how-to-use-postgresql-with-your-django-application-on-ubuntu-14-04) to run PostgreSQL database.
PostgreSQL provides much better searching, indexing and scaliblity options.

Configure your Database settings in settings.py to run the database. Assign DEBUG False and configure the Apache/Nginx to host the django app, PostgreSQL database and required static files.

Finally run

```
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver
```

in the directory which has manage.py to get your site up and running.


## Built With

* [Django](https://www.djangoproject.com/) - A python-based web framework
* [PostgreSQL](https://www.postgresql.org/) -  A powerful, open source object-relational database system


Feel free to test and contribute

Start the Django test server

```
python manage.py runserver
```

Change the database settings in *settings.py* in *faculty_portal* folder

## Authors

**Pavan Kumar** @pavan71198

**Saikiran Reddy** @saikiranreddysaikiran

**Shubhanker Jauhari** @Shubhanker99

**Hari Boddu** @hariboddu
