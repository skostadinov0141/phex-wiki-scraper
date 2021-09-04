from json import encoder
from os import replace
import os
import requests
import json
from urllib.parse import unquote
from bs4 import BeautifulSoup

if 'wiki_data.json' in os.listdir():
    os.remove("wiki_data.json")
with open('wiki_data.json',"a+") as f:
    f.write('{}')
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 OPR/78.0.4093.186'}
urls = open('links.txt',"r").readlines()
data = {}
completedTasks = 0
allTasks = len(urls)
for link in urls:
    updatedLink = link.replace('\n',"")
    r = requests.get(updatedLink)
    r.encoding = 'utf-8'
    #print(r.text)
    soup = BeautifulSoup(r.text, 'html.parser')
    soup.encode_contents(encoding='utf8')

    spellBody = soup.find('div',{'class':'body'})
    if spellBody != None:
        spellList = spellBody.find_all('a',href=True)
        for item in spellList:
            spellName = item.text
            spellLink = item['href']
            data[spellName] = 'https://www.ulisses-regelwiki.de/' + unquote(spellLink)
    else:
        spellBodies = soup.find_all('a',{'class':'ulSubMenu'})
        for item in spellBodies:
            spellName = item.text
            spellLink = item['href']
            data[spellName] = 'https://www.ulisses-regelwiki.de/' + unquote(spellLink)
    completedTasks += 1
    print('Completed tasks: ' + str(completedTasks) + " / " + str(allTasks))
jsonFile = open('wiki_data.json',"w",encoding='utf8')
json.dump(data,jsonFile,indent=4,ensure_ascii=False)