#!/usr/bin/env python
import os, sys
import requests
from bs4 import BeautifulSoup as bs4
from pdb import set_trace as debug

for requirement in [line.split("==")[0] for line in open("requirements.txt").read().split("\n") if line.split("==")[0]]:
    os.system("pip install --upgrade {0}".format(requirement))

localPythonVersion = sys.version.title().split()[0]
pythonDownloadURL = "https://www.python.org/downloads/"
pythonDownloadHTML = requests.get(pythonDownloadURL)
soup = bs4(pythonDownloadHTML.content, "html.parser")
link = soup.findAll('a', attrs={"class":"button"})[1].text
latestAvailablePythonVersion = link.split()[-1]
if localPythonVersion != latestAvailablePythonVersion:
    print "Your installed python version is {0} and the latest available is {1}.".format(localPythonVersion, latestAvailablePythonVersion)
