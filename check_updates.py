# Importing libraries

import sys
import time
import hashlib
import urllib
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
 
def CheckUpdates(): 
    # setting the URL you want to monitor
    url = Request('http://co.wayne.in.us/clerk/election/results.html',
                  headers={'User-Agent': 'Mozilla/5.0'})
     
    # to perform a GET request and load the
    # content of the website and store it in a var
    response = urlopen(url).read()
     
    # to create the initial hash
    currentHash = hashlib.sha224(response).hexdigest()
    print("running")
    time.sleep(10)
    while True:
        try:
            # perform the get request and store it in a var
            response = urlopen(url).read()
             
            # create a hash
            currentHash = hashlib.sha224(response).hexdigest()
             
            # wait for 30 seconds
            time.sleep(30)
             
            # perform the get request
            response = urlopen(url).read()
             
            # create a new hash
            newHash = hashlib.sha224(response).hexdigest()
     
            # check if new hash is same as the previous hash
            if newHash == currentHash:
                continue
     
            # if something changed in the hashes
            else:
                # notify
                scraper()
     
                # again read the website
                response = urlopen(url).read()
     
                # create a hash
                currentHash = hashlib.sha224(response).hexdigest()
     
                # wait for 30 seconds
                time.sleep(30)
                continue
                 
        # To handle exceptions
        except Exception as e:
            print("error")

def Scraper():

    text_file = 'LOCATION_OF_TEXT_FILE_YOU_WANT_SAVED' 				# <-- Change me!
    web_page = 'https://www.co.wayne.in.us/clerk/election/cumulative.html'
    page = urllib.request.urlopen(web_page)
    soup = BeautifulSoup(page, 'html.parser')

    original_stdout = sys.stdout # Save a reference to the original standard output

    # Names: span a292, Titles: span a93, vote percentage: div a346
    ballots = soup.find_all(True, class_=['a40', 'a43'])
    with open(text_file, 'w') as f:
        sys.stdout = f

        for i in ballots:
            if i.string.isnumeric():
                print(i.string)
                print('')
            else:
                print(i.string + ' = ' + i.string, end='    ')


        polling_places = soup.find_all(True, class_=['a46', 'a49'])

        for y in polling_places:
            if 'of 14' in y.string:
                print(y.string)
                print('')
            else:
                print(y.string + ' = ' + y.string, end='    ')



        names_titles = soup.find_all(True, class_=['a292', 'a93', 'a342', 'a346'])
            
        for x in names_titles:
            
            if x.string.isnumeric() or '%' in x.string or ',' in x.string:
                if '%' in x.string:
                    print(x.string)
                    print('')
                else:
                    print(x.string, end='    ')
            elif 'Vote' in x.string:
                if 'One' in x.string:
                    print(x.string[:-24] + ' = ' + x.string[:-24])
                    print('')
                elif 'Three' in x.string:
                    print(x.string[:-46] + ' = ' + x.string[:-46])
                    print('')
                elif 'Six' in x.string:
                    print(x.string[:-23] + ' = ' + x.string[:-23])
                    print('')
                else:
                    print(x.string, end='')
            else:
                print(x.string + ' = ' + x.string, end='    ')

        sys.stdout = original_stdout
        f.close()

Scraper()