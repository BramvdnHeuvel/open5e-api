# open5e is being rebuilt in Django and Vue.js!

Open5e is a community project driven by a small number of volunteers in their spare time. We welcome any and all contributions! Please join our Discord to help out: https://discord.gg/9RNE2rY or check out the issue board if you'd like to see what's being worked on!

The Django API uses Django REST Framework for its browsability and ease of use when developing CRUD endpoints.  It uses django's default SQLite database, and pulls the data from the /data directory.

# Quickstart
The API uses docker-compose to run, and by default binds https:// on port 443, which may not work for your system (I believe windows has problems binding on low ports.)  Here's the default command, run from the root.
> docker-compose up

This will allow you to access the project on https://localhost.

If you'd like to use docker and docker-compose for development, I would suggest rebinding the ports. Here's an example command that would allow for running the project on a non-standard port.

> docker-compose run --publish 8888:8888 server

This command runs the Server module (defined in docker-compose.yml), binding the port 8888 to 8888 locally.  This should allow you to access the site on https://localhost:8888.

# Development using Django Server
To do any python development on the django application itself, I would suggest using django's built-in server as it allows for various things (such as debug mode and quick reloads).  Here's the general process for getting that up and running.

First, install pipenv from here (https://pipenv.readthedocs.io/en/latest/). 

Once pipenv is installed locally, you can then use it to install of the project dependencies defined in the Pipfile.
> pipenv install

Then you will need to use the built-in django migration function to define your database, making sure to run it within the pipenv environment.
> pipenv run python manage.py migrate

You will then need to collect the static files (this makes django-resk-framework look presentable when viewing it in html).
> pipenv run python manage.py collectstatic --noinput

Finally, you will need to load the SRD data from the json files in the /data folder.  This is using the custom populatedb command.
> pipenv run python manage.py populatedb --flush ./data/WOTC_5e_SRD_v5.1/

At that point, you will be able to run the django server normally (within the pipenv environment).
> pipenv run python manage.py runserver

And your server should be available at http://localhost:8000.