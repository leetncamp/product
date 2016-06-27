#!/usr/bin/env python
# encoding: utf-8

import os
import sys
from pdb import set_trace as debug
stop = debug

from django.conf import settings

from django.core.wsgi import get_wsgi_application
os.environ['DJANGO_SETTINGS_MODULE'] = 'project.settings'
application = get_wsgi_application()
from django import setup
#os.chdir(os.path.dirname(__file__))
setup()
from hierarchy.models import *



from argparse import ArgumentParser
parser = ArgumentParser()
parser.add_argument("--codes", action="store_true", help="Add igor codes")
ns = parser.parse_args()




if ns.codes:
    #Only do this on a new database
    codes = """1-INSTRUMENT
2-UNKNOWN-DESC
3-CONSUMABLE
4-ACCESSORY
5-SERVICE PART
7-OLIGO
8-RENTAL
9-OTHER
A-SOFTWARE
B-TESTING/RESEARCH SERVICE
C-CONSULTING SERVICES
E-SVC BILLABLE LABOR
F-SERVICE CONTRACT
H-SERVICE TRAINING
J-UNKNOWN-DESC
K-SUPPORT SERVICE CONTRACT
L-SUBSCRIPTION CONTRACT
M-FREIGHT
Q-SERVICE QUALIFICATION
R-UNKNOWN-DESC
S-CONTRACT CLEARING
U-SOFTWARE PACKAGE
V-INSTRUMENT PACKAGE
W-CONSUMABLE PACKAGE
X-CUSTOM PACKAGE
Y-SERVICE PACKAGE""".split("\n")
    for line in codes:
        split = line.split("-")
        igor, created = IgorItemClass.objects.get_or_create(name=split[0], description=split[1])
        if created:
            igor.save()
    print("Loaded Igor Classes")
