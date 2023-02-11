import os
import sys
import json
import requests

WRITEUPS_LIST = os.path.join(os.getcwd(), 'data', 'writeups.json')
LAST_RECORDED_WRITEUP = os.path.join(os.getcwd(), 'data', 'last_writeup.json')
PENTESTER_LAND_URL = 'https://pentester.land/writeups.json'

def print_banner():
    print('''------------------------------------------

BBW created by Nehal (https://github.com/Nehal-Zaman)

------------------------------------------''')

def save_writeup_list(data, filename):
    '''
    Nice utility function to save a writeup list.
    '''
    try:
        # if the 'data' directory is not present,
        # it'll be created.
        if 'data' not in os.listdir(os.getcwd()):
            os.mkdir(os.path.join(os.getcwd(), 'data'))

        with open(filename, 'w') as wf:
            wf.write(json.dumps(data))
        return True
    except Exception as e:
        print(f'Can not save writeup list: {e}')
        return False
    
def print_writeup(writeup):
    print(f"""Title   : {writeup['Links'][0]['Title']}
Link    : {writeup['Links'][0]['Link']}
Authors : {', '.join(writeup['Authors'])}
Programs: {', '.join(writeup['Programs'])}
Bugs    : {', '.join(writeup['Bugs'])}
Bounty  : {writeup['Bounty']}
Date    : {writeup['PublicationDate']}
------------------------------------------""")

def get_fresh_writeup_list():
    '''
    Makes an HTTP request to Pentester.land and
    returns the list of writeups on the website.
    '''
    try:
        response = requests.get(PENTESTER_LAND_URL)
        return json.loads(response.content.decode('UTF-8'))
    except Exception as e:
        print(f'Can not get fresh writeups list: {e}')
        return None

def get_last_writeup_list():
    '''
    Returns the content of last fetched witeups list.
    If the list is not present, fresh list of writeups 
    is saved and returned.
    '''
    try:
        if not os.path.exists(WRITEUPS_LIST):
            print('Last dump of writeup not found. Making a fresh one.')
            writeups = get_fresh_writeup_list()
            if writeups:
                save_writeup_list(writeups, WRITEUPS_LIST)
                return writeups
            return None
        else:
            with open(WRITEUPS_LIST, 'r') as rf:
                return json.loads(rf.read())
    except Exception as e:
        print(f'Can not get list of last writeups: {e}')
    return None

def parse_latest_writeups(old_writeups):
    '''
    Parses through the last writeup dumps
    to find the new writeups
    '''
    latest_writeups = []
    fresh_writeups = get_fresh_writeup_list()

    if not fresh_writeups:
        sys.exit()

    save_writeup_list(fresh_writeups, WRITEUPS_LIST)

    if os.path.exists(LAST_RECORDED_WRITEUP):
        with open(LAST_RECORDED_WRITEUP, 'r') as rf:
            last_writeup = json.loads(rf.read())
        
        if last_writeup:
            for fresh_writeup in fresh_writeups['data']:
                if last_writeup != fresh_writeup:
                    latest_writeups.append(fresh_writeup)
                else:
                    break

    else:
        save_writeup_list(old_writeups['data'][0], LAST_RECORDED_WRITEUP)
        latest_writeups.append(old_writeups['data'][0])
        
    if len(latest_writeups) > 0:
        save_writeup_list(latest_writeups[0], LAST_RECORDED_WRITEUP)

    return latest_writeups 

def run_bbw():
    # Get the latest writeups
    writeups = get_last_writeup_list()
    # helper.save_writeup_list(writeups['data'][5], helper.LAST_RECORDED_WRITEUP)
    latest_writeups = parse_latest_writeups(writeups)
    
    if len(latest_writeups) > 0:
        for writeup in latest_writeups:
            print_writeup(writeup)
    else:
        print('No new writeups found.\n')