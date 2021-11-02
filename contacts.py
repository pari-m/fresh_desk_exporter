from datetime import datetime
import constants
from json import JSONDecodeError
import json
import os
import requests
from requests.auth import HTTPBasicAuth
import time
from urllib.parse import urljoin
from pymongo import MongoClient

api_key = constants.api_key
domain = constants.domain
password = constants.password


def get_ticket_list():
    r = requests.get("https://"+ domain +".freshdesk.com/api/v2/tickets/", auth = (api_key, password))
    if r.status_code == 200:
        print("Request processed successfully, the response is given below")
        print(r.content)

def get_ticket(ticket_id):
    retry = True
    while (retry):
        try:
            r = requests.get("https://"+ domain +".freshdesk.com/api/v2/tickets/"+ticket_id, auth = (api_key, password))
            response = json.loads(r.content)
            print(response)

            for key in response.keys():
                print(key)
            retry = False
        except (JSONDecodeError, ValueError) as e:
            if response.status_code == 429:
                seconds = int(response.text.split(' ')[2])
                print("Throttle limit reached, count reset in {} seconds. Sleeping".format(seconds))
                time.sleep(seconds + 1)
            else:
                raise e


def main():
    get_ticket_list()
    ticket_id = "2244"
    get_ticket(str(ticket_id))


if __name__ == '__main__':
    main()

