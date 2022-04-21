import requests, urllib3
import json
from pathlib import Path
from json import load

http = urllib3.PoolManager()

with Path("bot_config/unb_token.json").open() as f:
    config = load(f)

token = config["token"]
init_link = config["init_link"]


def checkBalance(gamblerID):
    credit_link = init_link + str(gamblerID)
    unb_cred = requests.get(credit_link,
                            headers={'Authorization': token},
                            params={'q': 'requests+language:python'})
    set1 = unb_cred.json()
    cash = set1.get('cash')
    return int(cash)


def unbAPI(amount, reason, gamblerID):
    credit_link = init_link + str(gamblerID)
    unb_cred = requests.patch(credit_link, data=json.dumps({'cash': amount, 'reason': reason}),
                              headers={'Authorization': token}, params={'q': 'requests+language:python'})
    credit = unb_cred.json()
    print(f"{reason}: {credit}")


def convert(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    if minutes == 0:
        return f"{seconds}s"
    elif hour == 0:
        return f"{minutes}m {seconds}s"
    else:
        return f"{hour}h {minutes}m {seconds}s"
