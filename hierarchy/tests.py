from django.test import TestCase
from hierarchy.models import *
import os
import requests

# Create your tests here.

class ImportExportTestCase(TestCase)
    def setUp(self):
        os.system(""./resetDB")
