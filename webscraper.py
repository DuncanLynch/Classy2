import sqlite3
from bs4 import BeautifulSoup, SoupStrainer
import requests
import json
import asyncio
import time

t = time.time() 

def addorupdate(dic: dict):
    dep = dic["classtype"]
    code = dic["classcode"]
    global t
    try:
        connection = sqlite3.connect("classdata.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM classes WHERE classtype = ? AND classcode = ?", (dic["classtype"], dic["classcode"]))
        info = cursor.fetchone()
        if info is None:
            cursor.execute("INSERT INTO classes (classtype, classcode, classtitle, classdescription, prerequisites, corequisites, typicallyoffered, credits) VALUES (?,?,?,?,?,?,?,?)", (str(dic["classtype"]), str(dic["classcode"]), str(dic["classtitle"]), str(dic["classdescription"]), str(dic["prerequisites"]), str(dic["corequisites"]), str(dic["typicallyoffered"]), str(dic["credits"]), str(dic["link"])))
            print(f"Successful update for {dic["classtype"]} {dic["classcode"]} | Process took {(time.time() - t):.2f} seconds to complete.")
        else:
            cursor.execute("UPDATE classes SET classtitle = ?, classdescription = ?, prerequisites = ?, corequisites = ?, typicallyoffered = ?, credits = ?, link = ? WHERE classtype = ? AND classcode = ?", ( str(dic["classtitle"]), str(dic["classdescription"]), str(dic["prerequisites"]), str(dic["corequisites"]), str(dic["typicallyoffered"]), str(dic["credits"]), str(dic["link"]), str(dic["classtype"]), str(dic["classcode"])))
            print(f"Successful update for {dic["classtype"]} {dic["classcode"]} | Process took {(time.time() - t):.2f} seconds to complete.")
        connection.commit()
    except:
        print(f"Insetion/Updating database failed for {dic["classtype"]} {dic["classcode"]} | Process took {(time.time() - t):.2f} seconds to complete.")
    t = time.time()
    cursor.close()

def removesecsigns(s: str) -> str:
    newstring = ""
    inside = False
    i = 0
    while i < len(s):
        if s[i] == "<":
            inside = True
        if not (s[i] == "\n" or inside):
            newstring += s[i]
        if s[i] == ">":
            inside = False
        i += 1
    return newstring


def parse(link: str, code: str):
    lootlist = []
    dbdict = {}
    dbdict["link"] = link
    dbdict["classtype"] = code.split(" ")[0]
    dbdict["classcode"] = code.split(" ")[1]
    r = requests.get(link)
    htmlsoup =  BeautifulSoup(r.content, 'html.parser', parse_only=SoupStrainer("div", attrs={"id": "main"})) #"sc-extrafield" "sc_coreqs" "credits" "desc" "main"
    soup = htmlsoup.prettify(encoding=None)
    l = ["sc-extrafield", "sc_coreqs", "sc_prereqs", "credits", "desc", "main"]
    l.reverse()
    for i in l:
        if i == "main":
            beginning = soup.find(f"<div id=\"{i}\">")
        else:
            beginning = soup.find(f"<div class=\"{i}\">")
        end = soup.find("</div>", beginning)
        p = removesecsigns(soup[beginning:end].strip())
        lootlist.append(p)
    if lootlist[0].strip() != "":
        dbdict["classtitle"] = lootlist[0].split(lootlist[1])[0].strip()
    else:
        dbdict["classtitle"] = ""
    if lootlist[1].strip() != "":
        dbdict["classdescription"] = lootlist[1].strip()
    else:
        dbdict["classdescription"] = ""
    if lootlist[3].strip() == "":
        dbdict["prerequisites"] = ""
    else:    
        dbdict["prerequisites"] = lootlist[3][lootlist[3].find("Prerequisite")+len("Prerequisite"):].strip()
    if lootlist[4].strip() == "":
        dbdict["corequisites"] = ""
    else:
        dbdict["corequisites"] = lootlist[4][lootlist[4].find("Corequisite")+len("Corequisite"):].strip()
    s = ""
    if lootlist[5].find("Fall") >= 0:
        s += "Fall Semester "
    if lootlist[5].find("Spring") >= 0:
        s += "Spring Semester"
    dbdict["typicallyoffered"] = s.strip()
    dbdict["credits"] = lootlist[2].strip()
    addorupdate(dbdict)


linkstem = "https://stevens.smartcatalogiq.com"

f = open('academic-catalogue.json')

data = json.load(f)

chilist = data["Children"]

coursedict = chilist[24]

for sec in coursedict["Children"]:
    for courselevel in sec["Children"]:
       for i in courselevel["Children"]:
          link = linkstem + i["Path"]
          parse(link.lower(), i["Name"])


#connection = sqlite3.connect("classdata.db")
#cursor = connection.cursor()
#cursor.execute("INSERT INTO classes (classtype, classcode, classtitle, classdescription, prerequisites, corequisites, typicallyoffered, credits) VALUES (?,?,?,?,?,?,?,?)", ("CS", "284", "CS 284   Data Structures", "", "CS 115", "CS 135", "Fall Semester Spring Semester", 3))
#connection.commit()
#connection.close()
print(f"Webscrape of the Stevens Academic Catalogue took {(time.time()):.2f}")
f.close()