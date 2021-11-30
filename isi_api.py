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

if __name__ == "__main__":
    PORT = 8080
    user = ""
    password = ""
    HEADERS = {'Content-Type': 'application/json'}
    OP = "GET"

    optlist, args = getopt(sys.argv[1:], 'hc:o:', ['--help', '--creds=', '--op='])
    for opt, a in optlist:
        if opt in ('-h', '--help'):
            usage()
        if opt in ('-c', '--creds'):
            (user, password) = a.split(':')
        if opt in ('-o', '--op'):
            if a.upper() in ('GET', 'POST', 'DELETE'):
                OP = a.upper()
            else:
                sys.stderr.write("Accepted ops are: GET, POST, DELETE\n")
                exit(1)
    if not user:
        user = python_input("User: ")
    if not password:
        password = getpass.getpass("Password: ")
    if OP in ("GET", "DELETE"):
        (host, endpoint) = args
    else:
        (host, data, endpoint) = args
    uri = "https://" + host + ":" + str(PORT)
    session = requests.Session()
    data = json.dumps({'username': user, 'password': password, 'services': ['platform']})
    resp = session.post(uri + '/session/1/session/', data=data, headers=HEADERS, verify=False)
    session.headers['referer'] = uri
    session.headers['X-CSRF-Token'] = session.cookies.get('isicsrf')
    print(session.headers)
    if OP == "GET":
        resp = session.get(uri + endpoint, verify=False)
        pprint(json.loads(resp.content))


