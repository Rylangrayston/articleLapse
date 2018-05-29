# save-webpage.py

import urllib2
import time
path = "site/"
from selenium import webdriver

DRIVER = 'chromedriver'
driver = webdriver.Chrome(DRIVER)

url = 'http://worldclock.com/'


nHTMLChecks= 0
response = urllib2.urlopen(url)
lastSite = response.read()
imageKeyFrameNumber = 0
htmlKeyFrameNumber = 0
htmlFileName = str( htmlKeyFrameNumber ) + ".html"
with open(path + htmlFileName,'w') as f:
    f.write(lastSite)


driver.get(url)
screenshot = driver.save_screenshot(  path + str(imageKeyFrameNumber) +  '.png')
driver.quit()


while True:
    time.sleep(20)
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
        DRIVER = 'chromedriver'
        driver = webdriver.Chrome(DRIVER)
        driver.get(url)
        time.sleep(5)
        screenshot = driver.save_screenshot(  path + str(imageKeyFrameNumber) +  '.png')
        driver.quit()


    else:
        print("no html or txt change detected at" + str( time.time() )  )

    if nHTMLChecks % 2 == 0:
        imageKeyFrameNumber += 1
        DRIVER = 'chromedriver'
        driver = webdriver.Chrome(DRIVER)
        driver.get(url)
        time.sleep(5)
        screenshot = driver.save_screenshot(  path + str(imageKeyFrameNumber) +  '.png')
        driver.quit()


