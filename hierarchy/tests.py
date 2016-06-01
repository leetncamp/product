from django.test import TestCase
from hierarchy.views import *
import os
from django.test import Client
from django.conf import settings
from django.core.management import call_command


# Create your tests here.

class ImportExportTestCase(TestCase):
    fixtures = ['codes.json', "auth.json"]
    def test_load(self):
        client = Client()
        existingXLSXpath = os.path.join(settings.BASE_DIR, "hierarchy", "uploads", "PRODUCT_HIERARCHY 2016.05.20f.xlsx")
        existingXLSX = open(existingXLSXpath, "rb")

        response = client.post("/uploadproducthierarchy", {'file':existingXLSX})
        print response.content
        debug()
