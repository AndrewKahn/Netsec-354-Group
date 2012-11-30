#!/usr/bin/env python
from urllib2 import build_opener, HTTPCookieProcessor, install_opener, urlopen
from multipart import MultipartPostHandler
from cookielib import CookieJar
from urllib import urlencode
from getpass import getpass
from time import sleep
import sys

DEBUG=False
SITE='netsec.cs.northwestern.edu'
LOGIN='https://netsec.cs.northwestern.edu/login/'
if DEBUG:
  SITE='localhost:8000'
  LOGIN='http://localhost:8000/login/'

def submit(project, file):
  cookies = CookieJar()
  opener = build_opener(HTTPCookieProcessor(cookies))
  install_opener(opener)

  username = raw_input('Username: ')
  password = getpass('Password: ')

  urlopen(LOGIN)
  urlopen(LOGIN, urlencode({
    'username': username,
    'password': password,
  }))
  
  url = 'http://%s/projects/%i/submit/' % (SITE, project)
  opener = build_opener(HTTPCookieProcessor(cookies), MultipartPostHandler)
  response = opener.open(url, {'file' : open(file, 'rb')})
  
  try:
    submission = int(response.read())
  except ValueError:
    sys.stderr.write('Invalid username and password\n')
    sys.exit(1)
    
  started = False
  count = -1
  while True:
    response = urlopen('http://%s/projects/status/%i/' % (SITE, submission))
    status = int(response.read())
    if status == 0: break
    elif status == 1:
      if not started:
        started = True
        if count > 0: sys.stderr.write('\n')
        sys.stderr.write('Testing started')
    elif count <= 0:
      if count == 0: sys.stderr.write('\n')
      sys.stderr.write('At position %i in queue' % (status-1))
      count = 10
    count -= 1
    sys.stderr.write('.')
    sleep(1)

  sys.stderr.write('\n')

  response = urlopen('http://%s/projects/result/%i/' % (SITE, submission))
  print response.read()

if __name__ == '__main__':
  submit(int(sys.argv[1]), sys.argv[2])