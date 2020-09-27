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
            "method": "delete",
            "identifiers": 
                {"value": "NIE"}
        },
    ]

    def test_initiliaze_qry(self):
        qry = core.QueryFactory().__call__(self.QUERIES[0])   
        assert(qry.__class__ == core.WriteQuery)     
        qry = core.QueryFactory().__call__(self.QUERIES[1])        
        assert(qry.__class__ == core.ViewQuery)     
        qry = core.QueryFactory().__call__(self.QUERIES[2])        
        assert(qry.__class__ == core.DeleteQuery)     


    def test_write_document_type(self):
        params = json.dumps([self.QUERIES[0]])        
        print(f"Write {write.WriteView().__call__(params)}")
        self.QUERIES[0]["defaults"] = {"value": "DNI"}        
        params = json.dumps([self.QUERIES[0]])        
        print(f"Update {write.WriteView().__call__(params)}")

    def test_view_document_type(self):                                   
        params = json.dumps([self.QUERIES[1]])        
        print(f"Update {view.ComputeView().__call__(params)}")

    def test_delete_document_type(self):                                   
        params = json.dumps([self.QUERIES[2]])        
        print(f"Delete {delete.DeleteView().__call__(params)}")

