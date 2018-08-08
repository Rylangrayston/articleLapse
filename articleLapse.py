# save-webpage.py

import urllib2
import time
import requests
import hashlib
import os
from selenium import webdriver
from PIL import Image
urlList = ["https://www.express.co.uk/news/uk/966524/english-defence-league-leader-tommy-robinson-jailed-contempt-of-court", "http://www.bbc.com/news/av/uk-england-leeds-44292139/tommy-robinson-arrested-outside-leeds-crown-court", "http://www.bbc.com/news/uk-england-leeds-44287640", "https://metro.co.uk/2018/05/29/tommy-robinson-jailed-13-months-contempt-court-7587545/", "https://metro.co.uk/2018/05/28/tommy-robinson-arrested-7583101/"]

class Page():
    def __init__(self, url, jobNumber):
        self.url = url
        self.jobNumber = jobNumber
        self.lastSite = None
        self.count = 0
        self.currentSite = None
        self.htmlKeyFrameNumber = 0
        self.imageKeyFrameNumber = 0
        self.path = "./" + str(self.jobNumber) + "/"
        self.imagePath = self.path + "screenShots/"
        #self.fileName = "job" + str(jobNumber)
        self.htmlFileName = "recordedHTML"
        self.nHTMLChecks = 0
        

    def getScreenShot(self):
        self.imageKeyFrameNumber += 1
        self.imageFileNamePNG = self.imagePath + str(self.imageKeyFrameNumber) +  ".png"
        self.imageFileNameJPG = self.imagePath + str(self.imageKeyFrameNumber) +  ".jpg"
        DRIVER = 'chromedriver'
        driver = webdriver.Chrome(DRIVER)
        driver.get(self.url)
        time.sleep(5)
        if not os.path.exists(self.imagePath):
            os.mkdir(self.imagePath)
        screenshot = driver.save_screenshot(self.imageFileNamePNG)
        driver.quit()
        time.sleep(1)

        im = Image.open(self.imageFileNamePNG)
        rgb_im = im.convert('RGB')
        rgb_im.save(self.imageFileNameJPG)




    def checkSite(self):
        print("loadingSite")
        response = urllib2.urlopen(url)
        self.currentSite = response.read()
        self.nHTMLChecks += 1
        print("checking For Change in html and text content ( may not inclued swaped images ) ")
        if not self.currentSite == self.lastSite:
            self.htmlKeyFrameNumber += 1
            self.htmlFileName = str( self.htmlKeyFrameNumber ) + ".html"
            print("change detected and saved as " + self.htmlFileName )
            if not os.path.exists(self.path):
                os.mkdir(self.path)
            with open(self.path + self.htmlFileName,'w') as f:
                f.write(self.currentSite)
            self.lastSite = self.currentSite
            self.getScreenShot()
            sendImage(self.imageFileNameJPG, self.jobNumber)
        else:
            print("no html or txt change detected at" + str( time.time() )  )

        if self.nHTMLChecks % 2 == 0:
            self.getScreenShot()
            sendImage(self.imageFileNameJPG, self.jobNumber)

def sendImage(fileName, jobNumber):
    try:
        with open(fileName, 'rb') as f:
            fileData = f.read()
            md5 = hashlib.md5(fileData).hexdigest()
            success = False
            wait = 1
            while not success:
                print(" attempting to send image growing video server")
                timeAtSendStart = time.time()
                r = requests.post('http://timelapse.eriktetland.com/images',
                    files={'file': fileData},
                    data = {
                        'md5':md5,
                        'job':jobNumber,
                        'filename':fileName
                    })
                # print(md5)
                # print(fileData)
                # print("sent image, got response: ")
                if(r.status_code == 202):
                    success = True
                    transmitionDuration = time.time() - timeAtSendStart
                    print( "sent Image successfully to growing video server in " + str(transmitionDuration) + " seconds")
                else:
                    print(r.status_code)
                    print(r.text)
                    print('failed to send to growing video server, waiting for '+ str(wait)+' seconds')
                    time.sleep(wait)
                    wait = min(wait * 2, 3600)
    except Exception as e:
        print "-----Warning could not Send Image ", e



jobNumber = 0
pageList = []
for url in urlList:
    jobNumber += 1
    pageList.append(Page(url, jobNumber))

print( "watching the folowing urls:")
for page in pageList:
    print(page.url)

time.sleep(10)


while True:
    print("------------------MAIN LOOP------------------")
    for page in pageList:
        page.checkSite()
    time.sleep(20)



#     # Save HTML
#     directory = 'directory_to_save_webpage_content/'
#     url = 'http://www.google.com'
#     wget = "wget -p -k -P {} {}".format(directory, url)
#     os.system(wget)

# wget -p -k -P robots=off --random-wait --user-agent="Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)" inHere http://www.bbc.com/news/world-europe-44289404

# wget  --random-wait  -r  -p  -e  robots=off  -U  mozilla 
