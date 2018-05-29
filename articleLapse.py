# save-webpage.py

import urllib2
import time


import requests
import hashlib

path = "site/"
from selenium import webdriver

url = 'http://worldclock.com/'

def sendImage(fileName):
    with open(fileName, 'rb') as f:
        fileData = f.read()
        md5 = hashlib.md5(fileData).hexdigest()
        success = False
        wait = 1
        while not success:
            print(" attempting to send image growing video server")
            r = requests.post('http://207.246.82.246/jobs/1', files={'file': fileData}, data = {'md5':md5})
            # print(md5)
            # print(fileData)
            # print("sent image, got response: ")
            # print(r.status_code)
            # print(r.text)
            if(r.status_code == 202):
                success = True
                print( "sent Image successfully to growing video server")
            else:
                print('failed to send to growing video server, waiting for '+ str(wait)+' seconds')
                time.sleep(wait)
                wait = min(wait * 2, 3600)

def getScreenShot(fileName):
    DRIVER = 'chromedriver'
    driver = webdriver.Chrome(DRIVER)
    driver.get(url)
    time.sleep(5)
    screenshot = driver.save_screenshot(fileName)
    driver.quit()


nHTMLChecks= 0
lastSite = None

htmlKeyFrameNumber = 0
imageKeyFrameNumber = 0

while True:
    print("loadingSite")
    response = urllib2.urlopen(url)
    currentSite = response.read()
    nHTMLChecks += 1
    print("checking For Change in html and text content ( may not inclued swaped images ) ")
    if not currentSite == lastSite:
        htmlKeyFrameNumber += 1
        fileName = str( htmlKeyFrameNumber ) + ".html"
        print("change detected and saved as " + fileName )
        with open(path + fileName,'w') as f:
            f.write(currentSite)
        lastSite = currentSite

        imageKeyFrameNumber += 1
        imageFileName = path + str(imageKeyFrameNumber) +  '.png'
        getScreenShot(imageFileName)
        sendImage(imageFileName)
    else:
        print("no html or txt change detected at" + str( time.time() )  )

    if nHTMLChecks % 2 == 0:
        imageKeyFrameNumber += 1
        imageFileName = path + str(imageKeyFrameNumber) +  '.png'
        getScreenShot(imageFileName)
        sendImage(imageFileName)
    time.sleep(20)
