Trelleux
========

Trelleux is a Django app that makes Trello behave like TeuxDeux. It:

* Ensures there is a Trello list for each day in the next N (=30) days.
* Shunts cards in lists from prior days to today.
* Archives lists from prior days.

Yeah I know Trello has due dates for cards, but this is much more visible. Works a treat in the mobile apps too.

To use:
-------

`pip install -r requirements.txt`

Create a database.

Create a Trello list that you want to use for your day-to-day tasks (I call mine 'To Do').

Copy `settings/local.tmpl.py` to `settings/local.py`. Configure `local.py` to your liking - you'll need to configure your database, and put your Trello developer key in.

Run the app and visit /admin/trelleux/trelloboard/.

You need to create a new record with the Board ID and the Client auth token. Choose your timezone (so it knows when the days change).

Run `./manage.py update_lists` and watch it do its thing on your boards.

If you want to keep it, put it on a server, and call `update_lists` every day at local midnight, or every hour if you have boards in several timezones.

TODO:
-----

* Make a public form to allow people to add their own boards.
* Create/update due dates (instead?)
* Factor out Trello API into its own project
* Create recurring cards
* iCal sync(!)
* when creating a new board, make it empty
* make certain labels skip weekends