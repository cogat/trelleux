To configure:
-------------

Copy ``dev.tmpl.env`` to ``dev.env`` and set your settings.

These variables will be used to set up the docker containers. If you change them
after running ``docker-compose up`` the first time, it may be best to remove and
rebuild the containers. This is particularly the case with changing usernames
and passwords.

To install:
-----------

Run a server::

   docker-compose up --build

Create the DB:

   docker exec -ti celerytemplate_django_1 ./manage.py migrate

Create an admin user::

   docker exec -ti celerytemplate_django_1 ./manage.py createsuperuser

Visit ``http://localhost:8000/admin/`` and log in.
