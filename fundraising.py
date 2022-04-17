# run using python3 fundraising.py
# pip3 install beautifulsoup4
# pip3 install lxml
# pip3 install firebase_admin

import requests
from bs4 import BeautifulSoup
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("firebase_key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()  
collection = db.collection('fundraise') 

url = "https://campaigns.vibha.org/campaigns/vibha-striders-2022"

r = requests.get(url)
html = r._content

parsed_html = BeautifulSoup(html, "lxml")
cards = parsed_html.body.findAll('div', attrs={'class':'card card-chart'})
for card in cards:
    content = card.find('div', attrs={'class':'card-content'})
    
    # Find the campaign owner's name    
    name = card.find('span', attrs={'class':'owner'}).get_text()

    # Find the campaign url
    url = card.find('div', attrs={'class':'card-footer'}).a.get('href')
    url = "https://campaigns.vibha.org" + url

    # Find the fundraising amounts
    amount = content.find('h3', attrs={'class':'title'}).get_text()
    raised = amount.split("/")[0].strip()
    target = amount.split("/")[1].strip()
    
    # Print everythingß
    #print(name + "=" + raised + "/" + target + " - " + url)
    res = collection.document(name).set({
        'raised' : raised,
        'target' : target,
#        'url' : url,
    }, merge=True)