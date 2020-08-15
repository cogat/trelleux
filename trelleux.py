import os
from trello import Client
from datetime import datetime, timedelta
import pytz

TRELLO_APP_KEY = os.environ['TRELLO_APP_KEY']
TRELLO_SECRET = os.environ['TRELLO_SECRET']
BOARD_IDS = os.environ['BOARD_IDS'].split(',')
DAYS_IN_FUTURE = int(os.environ['DAYS_IN_FUTURE'])
CLIENT_AUTH_TOKEN = os.environ['CLIENT_AUTH_TOKEN']
TIMEZONE = os.environ['TIMEZONE']

client = Client(app_key=TRELLO_APP_KEY, client_token=CLIENT_AUTH_TOKEN)


def update():
    for board_id in BOARD_IDS:
        print(f'updating board {board_id}')
        response = client.get(f'boards/{board_id}/lists', 'cards=open')

        # find target dates
        local_today = datetime.now(pytz.timezone(TIMEZONE)).date()
        target_dates = {(local_today + timedelta(n)) for n in range(DAYS_IN_FUTURE)}

        # find existing dates, and alexa list
        lists = response.json()
        existing_dates = {}
        past_lists = {}
        alexa_list = None
        for trello_list in lists:
            date_text = trello_list['name'][:10]
            try:
                d = datetime.strptime(date_text, '%Y-%m-%d').date()
                existing_dates[d] = trello_list
                if d < local_today:
                    past_lists[d] = trello_list
            except ValueError:
                # not a date list
                pass

            if trello_list['name'] == "From Alexa":
                alexa_list = trello_list

        # create lists for any missing dates
        missing_dates = target_dates - set(existing_dates.keys())
        for missing_date in missing_dates:
            datestr = f'{missing_date} ({d.strftime("%a")})'
            print(f'creating list {datestr}')
            response = client.post('lists', f'name={datestr}&idBoard={board_id}&pos=bottom')
            existing_dates[d] = response.json()

        today_list = existing_dates[local_today]

        # archive lists for past dates
        for d, l in past_lists.items():
            print(f'archiving {l["name"]}')
            response = client.post(
                f'lists/{l["id"]}/moveAllCards',
                f'idBoard={board_id}&idList={today_list["id"]}'
            )
            # archive the list
            response = client.put(f'lists/{l["id"]}', 'closed=true')

        # sort lists
        last_pos = None
        sort_remaining = False
        sorted_dates = sorted(existing_dates.keys())
        for d in sorted_dates:
            trello_list = existing_dates[d]
            pos = trello_list['pos']
            if last_pos is not None:
                if pos <= last_pos:
                    sort_remaining = True
            if sort_remaining:
                response = client.put(f'lists/{trello_list["id"]}', 'pos=bottom')
                last_pos = response.json()['pos']
            else:
                last_pos = pos

        # move cards from alexa list to today
        if alexa_list:
            response = client.post(
                f'lists/{alexa_list["id"]}/moveAllCards',
                f'idBoard={board_id}&idList={today_list["id"]}'
            )
            assert response.status_code == 200

            # move the alexa list to the end
            response = client.put(
                f'lists/{alexa_list["id"]}/pos',
                'value=bottom'
            )
            assert response.status_code == 200


if __name__ == '__main__':
    update()
