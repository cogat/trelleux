import os
from trello import Client
from datetime import datetime, timedelta
import pytz
from lis import longest_increasing_subsequence
from collections import OrderedDict
from multiprocessing import Process


TRELLO_APP_KEY = os.environ['TRELLO_APP_KEY']
TRELLO_SECRET = os.environ['TRELLO_SECRET']
CLIENT_AUTH_TOKEN = os.environ['CLIENT_AUTH_TOKEN']


def update_lists(client, board_id, days_in_future, timezone):
    processes = []
    print(f'updating board {board_id}')
    response = client.get(f'boards/{board_id}/lists')

    # find target dates
    local_today = datetime.now(pytz.timezone(timezone)).date()
    target_dates = {(local_today + timedelta(n)) for n in range(days_in_future)}

    # find existing dates, and alexa list
    lists = response.json()
    existing_dates = OrderedDict()
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
    missing_dates = sorted(target_dates - set(existing_dates.keys()))
    for missing_date in missing_dates:
        datestr = f'{missing_date} ({missing_date.strftime("%a")})'
        print(f'creating list {datestr}')
        if missing_date == local_today:
            # synchonously ensure a today list
            response = client.post(
                'lists',
                f'name={datestr}&idBoard={board_id}&pos=bottom'
            )
            existing_dates[local_today] = response.json()
        else:
            p = Process(target=client.post, args=(
                'lists',
                f'name={datestr}&idBoard={board_id}&pos=bottom'
            ))
            processes.append(p)
            p.start()

    today_list = existing_dates[local_today]

    # archive lists for past dates
    for d, l in past_lists.items():
        print(f'archiving {l["name"]}')
        # move all cards from the list to the today list
        p = Process(target=client.post, args=(
            f'lists/{l["id"]}/moveAllCards',
            f'idBoard={board_id}&idList={today_list["id"]}'
        ))
        processes.append(p)
        p.start()

        # archive the list
        p = Process(target=client.put, args=(
            f'lists/{l["id"]}',
            'closed=true'
        ))
        processes.append(p)
        p.start()

    # move cards from alexa list to today
    if alexa_list:
        print('clearing alexa list')
        p = Process(target=client.post, args=(
            f'lists/{alexa_list["id"]}/moveAllCards',
            f'idBoard={board_id}&idList={today_list["id"]}'
        ))
        processes.append(p)
        p.start()
        # move the alexa list to the end
        p = Process(target=client.put, args=(
            f'lists/{alexa_list["id"]}/pos',
            'value=bottom'
        ))
        processes.append(p)
        p.start()

    for process in processes:
        process.join()


def sort_lists(client, board_id):
    # sort lists
    # we do this efficiently by finding the longest increasing subsequence and
    # only making api calls for items not in the subsequence
    print('sorting')
    trello_lists = client.get(f'boards/{board_id}/lists').json()
    list_names = []
    list_data = {}
    for l in trello_lists:
        try:
            name = l['name']
            datetime.strptime(name[:10], '%Y-%m-%d')
            list_names.append(name)
            list_data[name] = l
        except ValueError:
            pass

    sorted_names = longest_increasing_subsequence(list_names)
    names_to_move = sorted(set(list_names) - set(sorted_names))

    processes = []
    for name_to_move in names_to_move:
        print(f'placing {name_to_move} in {len(sorted_names)} sorted names')
        # print(f'sorted_names={sorted_names}')

        # iterate through the sorted list until we find where the item should be inserted
        lower_i = None
        greater_i = None
        for i, item in enumerate(sorted_names):
            if item > name_to_move:
                greater_i = i
                break
            lower_i = i

        # print(f'{name_to_move} belongs between items {lower_i}, {greater_i}')

        try:
            lower_pos = list_data[sorted_names[lower_i]]['pos']
            # print(f' - above {sorted_names[lower_i]} ({lower_pos})')
        except TypeError:
            lower_pos = list_data[sorted_names[0]]['pos'] - 1000

        try:
            greater_pos = list_data[sorted_names[greater_i]]['pos']
            # print(f' - below {sorted_names[greater_i]} ({greater_pos})')
        except TypeError:
            greater_pos = list_data[sorted_names[-1]]['pos'] + 1000

        # update the pos to be the average of neighbouring items
        new_pos = (greater_pos + lower_pos) / 2
        assert lower_pos < new_pos < greater_pos
        list_data[name_to_move]['pos'] = new_pos

        p = Process(target=client.put, args=(
            f'lists/{list_data[name_to_move]["id"]}',
            f'pos={new_pos}'
        ))
        processes.append(p)
        p.start()

        # insert the item into the sorted list
        try:
            # print(f' - inserting at index {greater_i} ({new_pos})')
            sorted_names.insert(greater_i, name_to_move)
        except TypeError:
            # print(f' - inserting at end ({new_pos})')
            sorted_names.append(name_to_move)

    # print(f'sorted_names={sorted_names}')
    for process in processes:
        process.join()


def archive_empty_lists(client, board_id):
    print(f'archiving empty lists in {board_id}')
    response = client.get(f'boards/{board_id}/lists', 'cards=open')
    lists = response.json()
    processes = []
    for trello_list in lists:
        if not trello_list['cards']:
            # archive the list
            p = Process(target=client.put, args=(f'lists/{trello_list["id"]}', 'closed=true'))
            processes.append(p)
            p.start()
    for process in processes:
        process.join()
    print('done archiving')


def lambda_func(event, context):
    client = Client(app_key=TRELLO_APP_KEY, client_token=event['client_auth_token'])
    if 'archive_empty_lists' in event and event['archive_empty_lists']:
        archive_empty_lists(
            client,
            event['board_id']
        )
    update_lists(
        client=client,
        board_id=event['board_id'],
        days_in_future=event['days_in_future'],
        timezone=event['timezone'],
    )
    sort_lists(
        client,
        event['board_id']
    )

if __name__ == '__main__':
    lambda_func({
        'client_auth_token': CLIENT_AUTH_TOKEN,
        'board_id': '5f376d961dbcba31a070eaae',
        'days_in_future': 31,
        'timezone': 'Australia/Melbourne',
        'archive_empty_lists': True,
    }, None)
