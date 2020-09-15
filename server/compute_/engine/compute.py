import json
from datetime import datetime
from django.shortcuts import render
from django.http import Http404
from django.core.exceptions import PermissionDenied
from django.apps import apps
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from apicompute.serializers import GenericResultSet
from apicompute.views.utils.modelfuncwrapper import AggregationWrapper
from apicompute.views.utils.modelwrapper import ModelWrapper
from apicompute.views.utils.securityrules import SecurityRules
from django_pivot.histogram import histogram
from django.db.models.functions import *
from django.db.models import *
from django.contrib.auth.models import Group, Permission
from apiauth.models import Role
from apidata.models import ModelHierarchy


class ComputeView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def _get_model(self, qry: dict):
        models = apps.all_models["apidata"]
        return models[qry["table"]]

    def _get_agg_args(self, qry: dict) -> dict:
        res = dict()
        aggwrapper = AggregationWrapper()
        for arg in qry["aggfields"]:
            func = getattr(aggwrapper, arg["aggfunc"])
            aggfunc = func()
            fieldname = arg["fieldname"]
            res[arg["annotation"]] = aggfunc(fieldname)
        return res

    def _get_expressions(self, qry: dict) -> dict:
        res = dict()
        for expression in qry["expressions"]:
            # TODO using eval is considered as unsafe
            res[expression["name"]] = eval(expression["definition"])
        return res

    def _compute_multiset(self, qry: dict) -> list:
        try:
            nrows = qry["top"]
        except:
            nrows = None
        model = self._get_model(qry)
        expressions = self._get_expressions(qry)
        aggregations = self._get_agg_args(qry)
        sec = SecurityRules(model, self.request.user, ["view"])
        filters = Q(**qry["filters"]) & sec.rule        
        res = (
            model.objects.values(**expressions)
            .filter(filters)
            .values(*tuple(qry["categories"]))
            .annotate(**aggregations)
            .order_by(*tuple(qry["orderby"]))[:nrows]
        )
        res = {"result": [e for e in res], "name": qry["name"]}

        return res

    def _compute_hist(self, qry: dict) -> list:
        model = self._get_model(qry)
        expressions = self._get_expressions(qry)
        sec = SecurityRules(model, self.request.user, ["view"])
        filters = Q(**qry["filters"]) & sec.rule
        res = (
            model.objects.values(**expressions)
            .filter(filters)
            .values(*tuple([qry["categoryclasses"]]))
            .order_by(*tuple(qry["orderby"]))
        )
        res = histogram(res, qry["categoryclasses"], bins=[0, 1, 2])
        res = {"result": [e for e in res], "name": qry["name"]}

        return res

    def _compute_scalar(self, qry: dict) -> list:
        model = self._get_model(qry)
        aggregations = self._get_agg_args(qry)
        expressions = self._get_expressions(qry)
        sec = SecurityRules(model, self.request.user, ["view"])
        filters = Q(**qry["filters"]) & sec.rule
        res = (
            model.objects.values(**expressions)
            .filter(filters)
            .aggregate(**aggregations)
        )
        # TODO fast fix, output needs to be a list
        res = {"result": [res], "name": qry["name"]}

        return res
    
    def _compute_list(self, qry: dict) -> dict:
        model = self._get_model(qry)
        expressions = self._get_expressions(qry)
        sec = SecurityRules(model, self.request.user, ["view"])
        filters = Q(**qry["filters"]) & sec.rule
        res = (
            model.objects.values(**expressions)
            .filter(filters)
            .values(*tuple(qry["categories"]))
            .order_by(*tuple(qry["orderby"]))
            .distinct(*tuple(qry["orderby"]))
        )
        res = {"result": [e for e in res], "name": qry["name"]}
        return res

    def _qry_data(self, qry: dict) -> dict:
        if qry["type"] == "scalar":
            queryset = self._compute_scalar(qry)
        if qry["type"] == "multiset":
            queryset = self._compute_multiset(qry)
        if qry["type"] == "hist":
            queryset = self._compute_hist(qry)
        if qry["type"] == "list":
            queryset = self._compute_list(qry)
        if qry["type"] not in ["scalar", "multiset", "hist", "list"]:
            queryset = {"result": {"error": "Unkown query type"}, "name": qry["name"]}
        return queryset

    def _cast_queries_to_dict(self, queries) -> dict:
        data = queries.read()
        if type(data) == bytes and queries.content_type == "application/json":
            return json.loads(data)
        else:
            raise ValueError(
                "Parsing ERROR in queries. content_type has to be application/json."
            )

    def post(self, request, format=None):
        data = self.request.data
        queries = self._cast_queries_to_dict(data["queries"])
        querysets = list()        
        for qry in queries:
            querysets.append(self._qry_data(qry))
        serializer = GenericResultSet(querysets, many=True)
        return Response(serializer.data)
