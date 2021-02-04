import webbrowser
import json, os, sys
packman_url = 'https://www.google.com/logos/2010/pacman10-i.html'
def runPackman():
    # pacman is opened in browser
    webbrowser.register('chrome', None, webbrowser.BackgroundBrowser("C:\Program Files\Google\Chrome\Application\chrome.exe"))
    webbrowser.get('chrome').open_new(packman_url)
    
def jsonlocation():
    # location.json file is created if not in the memory
    f = open('location.json',) 
    data = json.load(f) 
    location = list(data)[0]
    f.close()
    location = '"' + location + '"'
    print(location)
    os.system(location)
