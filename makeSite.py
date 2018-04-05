from flask import Flask
import requests
import re
from bs4 import BeautifulSoup
app = Flask(__name__)

def writeWeb(webName):
	r = requests.get(webName)
	return(r.text)


def insertNav(fname):
	f = open(fname)
	newFile = f.read()
	f.close()
	splitFile = newFile.split("<div id=\"navbar\">")
	f = open("navbar.html")
	splitFile.insert(1, f.read())
	f.close()
	return "".join(splitFile)

def getCoolLinks():
	oriSite = writeWeb("https://www.coolmath-games.com/1-complete-game-list")
	soup = BeautifulSoup(oriSite, "html.parser")
	linkTags = []
	for i in soup.find_all("span"):
		eClass = i.get("class")
		if(eClass):
			if(eClass[0] == "game-title"):
				linkTags.append(i)
	allLinks = []
	for i in linkTags:
		link = i.find("a")
		if(link):
			allLinks.append(link.get("href"))
	return allLinks
coolLinks = getCoolLinks()

def deCoolmath(realSite):
	oriCool = writeWeb(realSite)
	for i in coolLinks:
		r = re.search(i, oriCool)
		if(r):
			coolSplit = oriCool.split(i)
			coolSplit.insert(1, "coolmath/")
			newCool = "".join(coolSplit)
	print(newCool)
	return newCool

@app.route("/")
def homePage():
	return insertNav("index.html")

@app.route("/coolmath")
def coolmath():
	return deCoolmath("https://www.coolmath-games.com/1-complete-game-list")