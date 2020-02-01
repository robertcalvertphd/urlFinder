from CSV_HELPER import *
from bs4 import BeautifulSoup
import requests
from ValidExtensions import DOMAINS

HEALTHY_URL = 200
def getAllLinks(url):
    ret = [] # creates return value as empty array
    page = requests.get(url) # loads the requested page using request library
    soup = BeautifulSoup(page.text, 'html.parser') #creates the soup variable as an instance
    # of the object BeautifulSoup which takes as an argument page.text and the instruction html.parser
    for link in soup.find_all('a'): #find attribute tags
        href = str(link.get('href')) #get href portion of attribute tag
        if not href == 'None': #confirms that data is not None
            validatedHREF = validateHREF(href,url,ret) #passes href over to validateFunction
            if validatedHREF: #href was validated
                ret.append(validatedHREF) #add it to the return array
    ret= removeRepeatedLinks(ret)
    return ret #return the array

def checkURL(url):
    response = requests.get(url)
    if response.status_code == HEALTHY_URL:
        #print("valid url")
        return 1
    else:
        #print("invalid url")
        return 0

def validateHREF(href, originalURL, currentList):
    # handle internal links that do not are of form /blog for example
    if href[0] == '/':
        href = handleInternalLinks(originalURL, href)
    #check for slashes
    href = handleEndingInSlashes(href)
    if href is None: return None
    #handle internal objects that are not .html but are attributes
    if href[0] == '#':
        return None
    ret = href
    if ret is not None:
        #remove items that may be downloaded
        ret = handleDownloads(href)
        #confirm ret is a valid link
        if ret is not None and checkURL(ret):
            return ret
    return None

def handleEndingInSlashes(original_href):
    href = original_href
    if not original_href.endswith("/"):
        href = original_href +  '/'
    return href

def removeRepeatedLinks(list):
    ret = []
    for item in list:
        if not ret.__contains__(item):
            ret.append(item)
    return ret

def handleInternalLinks(originalAddress, internalLink):
    secondForwardSlash = originalAddress.find('/')+2
    thirdForwardSlash = originalAddress.find('/',secondForwardSlash)
    return(originalAddress[:thirdForwardSlash]+internalLink)

def handleDownloads(href):
    numberOfPeriods = href.count(".")
    if numberOfPeriods > 1:
        lastperiodPosition = 0
        for period in range(numberOfPeriods):
            lastperiodPosition = href.find('.', lastperiodPosition+1)
        lastperiodPosition = lastperiodPosition+1
        extension = href[lastperiodPosition:-1]
        if extension == "html":
            return href[:-1]
        if DOMAINS.__contains__(extension.upper()):
            return href
        else:
            return None
    else:
        return href


def createCSVListFromURL(url):
    links = getAllLinks(url)
    createCSV(links)

def createCSV(links):
    listString = ""

    for link in links:
        listString += link + "," + "\n"
    s = listString[:-1]
    name = "CensusData"
    columnName = "LINK"

    extension = "csv"
    try:
        name = name + "." + extension
        file = open(name, 'a')
        file.write(columnName +"\n"+ s[:-1])
        file.close()
    except:
        print("error occurred")
        sys.exit(0)

url = 'https://www.census.gov/programs-surveys/popest.html'
createCSVListFromURL(url)