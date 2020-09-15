from .utils import collector
from .core import CoreComputeEngine, ViewQuery


class ComputeView(CoreComputeEngine):    
    
    def __init__(self, queries: str):
        super(ComputeView, self).__init__(queries)
    
    @collector("_qry_method","multiset")
    def _compute_multiset(self, qry: ViewQuery) -> dict:        
        res = (
            qry.model.objects.values(**qry.expressions)
            .filter(qry.identifiers)
            .values(*qry.categories)
            .annotate(**qry.aggregations)
            .order_by(*qry.orderby)[:qry.top_nrows]
        )
        res = {"result": [e for e in res], "name": qry.name, "method": qry.method}
        return res

    @collector("_qry_method","scalar")
    def _compute_scalar(self, qry: ViewQuery) -> dict:        
        res = (
            qry.model.objects.values(**qry.expressions)
            .filter(qry.identifiers)
            .aggregate(**qry.aggregations)
        )
        # TODO fast fix, output needs to be a list
        res = {"result": [res], "name": qry.name, "method": qry.method}

        return res
    
    @collector("_qry_method","list")
    def _compute_list(self, qry: ViewQuery) -> list:        
        res = (
            qry.model.objects.values(**qry.expressions)
            .filter(qry.filters)
            .values(*qry.categories)
            .order_by(*qry.orderby)
            .distinct(*qry.orderby)
        )
        res = {"result": [e for e in res], "name": qry.name, "method": qry.method}
        return res

    
