"""
Use https://github.com/keith/reminders-cli to post all reminders in the Inbox to the Today list
in Trello, and then clear the Inbox.
"""

from lib.trello import Client
from typing import List, Tuple
import subprocess
import os
import re
from datetime import datetime
import pytz

LIST_NAME = "Inbox"
LIST_ITEM_RE = r"(\d+): (.+)\n"

TRELLO_APP_KEY = os.environ["TRELLO_APP_KEY"]
CLIENT_AUTH_TOKEN = os.environ["CLIENT_AUTH_TOKEN"]
BOARD_ID = os.environ["BOARD_ID"]


TIMEZONE = "Australia/Melbourne"


def get_reminders(list_name: str) -> List[Tuple[str, str]]:
    """
    Return a list of tuples representing indexes and items
    """
    items_result = subprocess.run(["reminders", "show", list_name], capture_output=True)
    items = re.findall(LIST_ITEM_RE, items_result.stdout.decode())
    return items


def sync():
    client = Client(app_key=TRELLO_APP_KEY, client_token=CLIENT_AUTH_TOKEN)
    lists = client.get(f"boards/{BOARD_ID}/lists")
    local_today_iso = datetime.now(pytz.timezone(TIMEZONE)).date().isoformat()
    today_list_id = None
    for l in lists:
        if local_today_iso in l["name"]:
            today_list_id = l["id"]
            break

    items = get_reminders(list_name=LIST_NAME)
    for index, item in items:
        # post to trello
        client.post(f"cards", params=f"idList={today_list_id}&pos=bottom&name={item}")

    # since deleting by index changes the indices, let's delete in reverse
    for index, item in reversed(items):
        subprocess.run(["reminders", "complete", LIST_NAME, index], capture_output=True)


if __name__ == "__main__":
    sync()
