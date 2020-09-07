import json
from datetime import datetime
from django.shortcuts import render
from django.http import Http404
from django.apps import apps
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth.models import Group, Permission
from django.db.models.functions import *
from django.db.models import *
from apicompute.serializers import GenericResultSet
from apicompute.views.utils.modelfuncwrapper import AggregationWrapper
from apicompute.views.utils.modelwrapper import ModelWrapper
from apicompute.views.utils.securityrules import SecurityRules
from apiauth.models import Role
from apidata.models import ModelHierarchy


class DeleteView(APIView):  
    permission_classes = (permissions.IsAuthenticated,)

    def _get_model(self, qry: dict):
        models = apps.all_models["apidata"]
        return models[qry["table"]]

        
    def _delete_file(self, qry: dict) -> list:
        model = self._get_model(qry)        
        sec = SecurityRules(model, self.request.user, ["delete"])                
        filters = Q(**qry["identifiers"]) & sec.rule                
        counter, _ = model.objects.filter(filters).delete()
        if counter > 0:
            msg = "OBJ_DELETED"
        else:
            msg = "SPECIFIED_OBJ_NOT_FOUND"
        res = {"result": [{"status": "OK", "msg": msg}], "name": qry["name"]}            
        return res


    def _qry_data(self, qry: dict) -> dict:
        if qry["type"] == "delete":
            queryset = self._delete_file(qry)
        if qry["type"] not in ["delete"]:
            queryset = {"result": {"error": "Unkown query type"}, "name": qry["name"]}
        return queryset

    def _cast_queries_to_dict(self, queries) -> dict:
        data = queries.read()
        if type(data) == bytes and queries.content_type == "application/json":
            return json.loads(data)
        else:
            raise ValueError('Parsing ERROR in queries. content_type has to be application/json.')


    def post(self, request, format=None):
        data = self.request.data                
        queries = self._cast_queries_to_dict(data["queries"])
        querysets = list()
        for qry in queries:
            querysets.append(self._qry_data(qry))
        serializer = GenericResultSet(querysets, many=True)
        return Response(serializer.data)   