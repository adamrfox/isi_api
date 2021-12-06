#!/usr/bin/python

from __future__ import print_function
import sys
from getopt import getopt
import requests
import json
import getpass
from pprint import pprint
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def usage():
    print("Usage goes here!")
    exit(0)

def python_input(message):
    if int(sys.version[0]) > 2:
        val = input(message)
    else:
        val = raw_input(message)
    return (val)

def dprint(message):
    if DEBUG:
        print(message)

if __name__ == "__main__":
    PORT = 8080
    user = ""
    password = ""
    HEADERS = {'Content-Type': 'application/json'}
    OP = "GET"
    services = ['platform']
    DEBUG = False

    optlist, args = getopt(sys.argv[1:], 'hDc:o:s', ['--help', '--DEBUG', '--creds=', '--op=', '--services'])
    for opt, a in optlist:
        if opt in ('-h', '--help'):
            usage()
        if opt in ('-D', '--DEBUG'):
            DEBUG = True
        if opt in ('-c', '--creds'):
            (user, password) = a.split(':')
        if opt in ('-o', '--op'):
            if a.upper() in ('GET', 'POST', 'DELETE'):
                OP = a.upper()
            else:
                sys.stderr.write("Accepted ops are: GET, POST, DELETE\n")
                exit(1)
        if opt in ('-s', '--services'):
            services = a.split(',')

    if not user:
        user = python_input("User: ")
    if not password:
        password = getpass.getpass("Password: ")
    if OP in ("GET", "DELETE"):
        (host, endpoint) = args
    else:
        (host, data, endpoint) = args
        data_j = json.loads(data)
    uri = "https://" + host + ":" + str(PORT)
    session = requests.Session()
    data = json.dumps({'username': user, 'password': password, 'services': ['platform']})
    resp = session.post(uri + '/session/1/session/', data=data, headers=HEADERS, verify=False)
    session.headers['referer'] = uri
    session.headers['X-CSRF-Token'] = session.cookies.get('isicsrf')
    dprint("HEADERS: " + str(session.headers))
    if OP == "GET":
        resp = session.get(uri + endpoint, verify=False)
        pprint(json.loads(resp.content))
    elif OP == "DELETE":
        resp = session.delete(uri + endpoint, verify=False)
        if resp.status_code != 204:
            pprint(json.loads(resp.content))
    elif OP == "POST":
        resp = session.post(uri + endpoint, json=data_j, verify=False)
        if resp.status_code != 201:
            pprint(json.loads(resp.content))



