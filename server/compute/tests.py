from django.test import TestCase
import json
from .engines import write, view, delete, core
from .models import data as mdl

# Create your tests here.

class WriteTestCase(TestCase):

    QUERIES = [
        {
            "name": "Test Write Qry",
            "type": "write",
            "model": "documenttype",
            "method": "write_item",
            "identifiers": 
                {"value": "NIE"}
        },
        {
            "name": "Test View Qry",
            "type": "view",
            "model": "documenttype",
            "method": "multiset",
            "identifiers": 
                {"value": "NIE"}
        },
        {
            "name": "Test Delete Qry",
            "type": "delete",
            "model": "documenttype",
            "method": "write_item",
            "identifiers": 
                {"value": "NIE"}
        },
    ]

    def test_initiliaze_qry(self):
        qry = core.QueryFactory().__call__(self.QUERIES[0])        
        qry = core.QueryFactory().__call__(self.QUERIES[1])        
        qry = core.QueryFactory().__call__(self.QUERIES[2])        


    def test_write_document_type(self):
        params = json.dumps(self.QUERIES[:0])        
        print(f"Write {write.WriteView().__call__(params)}")

