from collections import OrderedDict
import json
from dateutil import parser
from datetime import datetime, timedelta
import pytz
from django.db import models
from timezone_field.fields import TimeZoneField
from django.conf import settings
from .trello import Client


class TrelloBoard(models.Model):
    client = models.ForeignKey('TrelloClient', related_name='boards')
    board_realid = models.CharField(max_length=255, help_text="Trello's real ID for this board. Discovered automatically if you don't know it", blank=True)
    timezone = TimeZoneField()
    enabled = models.BooleanField(default=True)
    fail_count = models.PositiveIntegerField(default=0)
    days_in_future = models.PositiveIntegerField(default=30)

    def __unicode__(self):
        return "Board %s" % self.board_realid

    def _dates_to_create(self, existing_dates, start_date, num_days):
        for n in range(num_days):
            d = start_date + timedelta(n)
            if d not in existing_dates:
                yield d

    def update_lists(self):
        client = self.client.get_client()
        response = client.get('boards/%s/lists' % self.board_realid, 'cards=open')
        if response.status_code == 200:
            lists = response.obj
        else:
            # It didn't work. We'll just increment a fail count for now.
            self.fail_count = self.fail_count + 1
            self.save()
            return

        """
        Now we have an (ordered) list of the lists on this Trello board.

        1. Ensure that we have created sufficient days in the future.
        2. Archive days in the past, moving outstanding items to today.
        3. Sort the days.
        """

        self.existing_dates = {}
        for l in lists:
            try:
                d = parser.parse(l['name'][:10]).date()
                self.existing_dates[d] = l
            except ValueError:
                pass

        self.local_today = self.timezone.normalize(datetime.utcnow().replace(tzinfo=pytz.utc)).date()
        self._ensure_dates()
        self._archive_past()
        self._sort_lists()

    def _ensure_dates(self):
        client = self.client.get_client()
        for d in self._dates_to_create(self.existing_dates, self.local_today, self.days_in_future):
            datestr = "%s (%s)" % (d, d.strftime("%a"))
            print "creating list '%s'" % datestr

            response = client.post('lists', 'name=%(NAME)s&idBoard=%(BOARD)s&pos=bottom' % {
                'BOARD': self.board_realid,
                'NAME': datestr,
            })
            self.existing_dates[d] = response.obj

    def _archive_past(self):
        """
        Archive lists that are in the past, moving any unarchived items to the top of the first list
        """
        client = self.client.get_client()
        today_list = self.existing_dates[self.local_today] #ensured by _ensure_lists
        drop_me = set()
        for d, l in self.existing_dates.iteritems():
            if d < self.local_today: #list is in the past
                drop_me.add(d)
                print "archiving '%s'." % l['name']
                # move all its cards to today
                response = client.get('lists/%s/cards' % l['id'], 'fields=')
                cards = response.obj
                for i, c in enumerate(cards):
                    response = client.put('cards/%s' % c['id'], 'idList=%s&pos=%s' % (today_list['id'], i+1 ))
                    assert response.status_code == 200

                # archive the list
                response = client.put('lists/%s' % l['id'], 'closed=true')
        #forget the lists I just archived
        for d in drop_me:
            del self.existing_dates[d]

    def _sort_lists(self):
        """
        Arrange lists into date order
        """
        client = self.client.get_client()
        def _date_sort(a, b):
            return (a[0] - b[0]).days
        list_by_date = OrderedDict(sorted(self.existing_dates.items(), cmp=_date_sort))
        last_pos = None
        sort_remaining = False
        for d, l in list_by_date.iteritems():
            pos = l['pos']
            if last_pos is not None:
                if pos <= last_pos:
                    print "sorting lists"
                    sort_remaining = True
            if sort_remaining:
                response = client.put('lists/%s' % l['id'], 'pos=bottom')
                last_pos = response.obj['pos']
            else:
                last_pos = pos


class TrelloClient(models.Model):
    client_auth_token = models.CharField(max_length=255, help_text='Visit <a href="https://trello.com/1/authorize?key=%s&name=Trelleux&expiration=never&response_type=token&scope=read,write">here</a> to get a token.' % settings.TRELLO_DEVELOPER_KEY, primary_key=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "Client created on %s" % self.date_created

    def get_client(self):
        if not hasattr(self, '_client'):
            self._client = Client(app_key=settings.TRELLO_DEVELOPER_KEY, client_token=self.client_auth_token)
        return self._client

    def get_boards(self):
        "return API boards that have database records (ie were created by Trelleux)"
        api_boards = self.get_client().get('member/me/boards/').obj
        model_boards = self.boards.filter()

        api_board_dict = {}
        for b in api_boards:
            api_board_dict[b['id']] = b

        result = []
        for b in model_boards:
            try:
                api = api_board_dict[b.board_realid]
                api['model_instance'] = b
                result.append(api)
            except:
                b.enabled = False
                b.save()

        return result

    def create_board(self):
        board = self.get_client().post("boards", "name=Trelleux Board")
        return self.boards.create(
            board_realid=board.obj['id']
        )
