from flask import Flask
from flask import request
from flask.json import jsonify
from flask.templating import render_template

import time
import os
import json
import multiprocessing
import urllib
import requests
import webbrowser
from lxml import html
from urllib.request import urlopen
from requests.sessions import session
from requests_html import HTML
from requests_html import HTMLSession
from linkClass import Link

def sub(url, queue):
    l = Link('', 0)
    try:
        page = requests.get(url)
        tree = html.fromstring(page.content)
        ele = tree.xpath('//*[contains(text(),"%")]')
        num = len(ele)
        if(num > 2):
            l = Link(url, num)
            print("completed " + url)
        else:
            print("insufficient data")
    except:
        print("error with page: " + url)

    queue.put(l)
        

def main(search):
    urlList = []
    query = urllib.parse.quote_plus(search)
    session = HTMLSession()
    response = session.get('https://www.google.com/search?q=' + query)
    links = list(response.html.absolute_links)
    google_domains = (  'https://www.google.', 
                        'https://google.', 
                        'https://webcache.googleusercontent.', 
                        'http://webcache.googleusercontent.', 
                        'https://policies.google.',
                        'https://support.google.',
                        'https://maps.google.',
                        'http://scholar.google.com',
                        'https://www.youtube.com'  )

    for url in links[:]:
        if url.startswith(google_domains):
            links.remove(url)
    
    processes = []

    queue = multiprocessing.Queue()
    for x in range(len(links)):   
        p = multiprocessing.Process(target=sub,args=(links[x],queue))
        processes.append(p)
        p.start()
        
    for p in processes:
        p.join()
        
    urlList = [queue.get() for p in processes]
    
    def n_sort(l):
        return (l.num)

    urlList = sorted(urlList, key=n_sort, reverse=True)
    urlList2 = []
    #webbrowser.open_new(urlList[0].link)
    for l in urlList:
        if(l.num > 2):
            urlList2.append(l)
    
    return(urlList2)

'''flask stuff'''

app = Flask(__name__)

@app.route("/")
def index():
    q = request.args.get('q')
    j = ""
    if q:
        j = main(q)
    return render_template("index.html", jsonText = j)

if __name__ == "__main__":
    app.debug = True
    app.run()

