import json
from datetime import datetime
from django.apps import apps
from compute.utils.collections import collector
from compute.core.engines import CoreComputeEngine


class ComputeView(CoreComputeEngine):    
    
    def __init__(self, queries: str):
        super(ComputeView, self).__init__(queries)
    
    @collector("multiset")
    def _compute_multiset(self, qry: dict) -> list:
        try:
            nrows = qry["top"]
        except:
            nrows = None
        model = self._get_model(qry)
        expressions = self._get_expressions(qry)
        aggregations = self._get_agg_args(qry)        
        filters = Q(**qry["filters"])
        res = (
            model.objects.values(**expressions)
            .filter(filters)
            .values(*tuple(qry["categories"]))
            .annotate(**aggregations)
            .order_by(*tuple(qry["orderby"]))[:nrows]
        )
        res = {"result": [e for e in res], "name": qry["name"]}
        return res

    @collector("scalar")
    def _compute_scalar(self, qry: dict) -> list:
        model = self._get_model(qry)
        aggregations = self._get_agg_args(qry)
        expressions = self._get_expressions(qry)
        filters = Q(**qry["filters"])
        res = (
            model.objects.values(**expressions)
            .filter(filters)
            .aggregate(**aggregations)
        )
        # TODO fast fix, output needs to be a list
        res = {"result": [res], "name": qry["name"]}

        return res
    
    @collector("list")
    def _compute_list(self, qry: dict) -> dict:
        model = self._get_model(qry)
        expressions = self._get_expressions(qry)
        filters = Q(**qry["filters"])
        res = (
            model.objects.values(**expressions)
            .filter(filters)
            .values(*tuple(qry["categories"]))
            .order_by(*tuple(qry["orderby"]))
            .distinct(*tuple(qry["orderby"]))
        )
        res = {"result": [e for e in res], "name": qry["name"]}
        return res

    
