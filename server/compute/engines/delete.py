from .utils import collector
from .core import CoreComputeEngine, DeleteQuery
from django.db.models import Q



class DeleteView(CoreComputeEngine):

    def __call__(self, queries: str): 
        return super(DeleteView, self).__call__(queries)

    @collector('_qry_method', 'delete')
    def _delete(self, qry: DeleteQuery) -> list:        
        counter, _ = qry.model.objects.filter(qry.identifiers).delete()
        if counter > 0:
            msg = "OBJ_DELETED"
        else:
            msg = "SPECIFIED_OBJ_NOT_FOUND"
        res = {"result": [{"status": "OK", "msg": msg}], "name": qry.name}            
        return res    