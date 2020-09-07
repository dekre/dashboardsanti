import json
import os
import re
from typing import List
from datetime import datetime
from django.shortcuts import render
from django.http import Http404
from django.apps import apps
from django.core.files.base import ContentFile
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.parsers import FileUploadParser, MultiPartParser
from apicompute.serializers import GenericResultSet
from apicompute.views.utils.modelfuncwrapper import AggregationWrapper
from apicompute.views.utils.modelwrapper import ModelWrapper
from apicompute.views.utils.securityrules import SecurityRules
from apidata.models.core import Item
from apidata.models.data import ProjectDocumentCollection
from django.contrib.auth.models import Group, Permission
from django.db.models.functions import *
from django.db.models import *
from _kep_backend.settings import MEDIA_URL, MEDIA_ROOT
from apiauth.models import Role
from apidata.models import ModelHierarchy


class CreateView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    parser_class = (
        FileUploadParser,
        MultiPartParser,
    )    

    def _get_model(self, qry: dict):
        models = apps.all_models["apidata"]
        return models[qry["table"]]    

    def _get_parent(self, qry: dict) -> object:
        model = self._get_model(qry)        
        obj = model.objects.get(**qry["identifiers"])
        return obj

    def _get_custodies(self, qry) -> List[Item]:
        res = list()
        for custody in qry["custodies"]:
            model = self._get_model(custody)
            obj = model.objects.get(**custody["identifiers"])
            res.append(obj)
        return res

    
    def _create_collection_role(self, obj: Item, qry: dict):               
        res = dict()
        if obj.is_collection:
            res["collection"] = {"label": obj._meta.label_lower, "id": obj.id}
            if "roles" in qry:
                r_ = list()
                for role_ in qry["roles"]:
                    role, created = Role.objects.get_or_create(
                        **role_["identifiers"], defaults=role_["defaults"]
                    )

                    if "inherit_from" in role_:
                        for inherit_role in role_["inherit_from"]:
                            inherit_role = Role.objects.get(**inherit_role["identifiers"])
                            role.inherit_from.add(inherit_role)

                    if "permissions" in role_:
                        for perm_ in role_["permissions"]:
                            perm = Role.objects.get(**perm_["identifiers"])
                            role.permissions.add(perm)

                    role.collections.add(obj)
                    role.user_set.add(self.request.user)                    
                    r_.append({"role": role.name, "created": created})
                res["roles"] = r_
        return res


    def _get_locale_file(
        self, path_to_file: str
    ) -> (
        str,
        str,
    ):
        path = os.path.join(MEDIA_ROOT, path_to_file)
        with open(path, "r", encoding="utf8") as f:
            content = f.read()
            f.close()
        file_name = os.path.basename(path)
        return content, file_name

    def _create_or_update_single_instance(self, qry) -> (Item, bool,):
        """
        Saves an item with given defaul values. 
        """
        model = self._get_model(qry)
        sec = SecurityRules(model, self.request.user, ["add","change"])
        if "parents" in qry:
            for parent in qry["parents"]:
                obj = self._get_parent(parent)
                # HERE - CHECK I PARENT ALLOWS CREATION OR IF PERMISSION IS GLOBALLY
                qry["identifiers"][parent["fieldname"]] = obj  
                qry["defaults"][parent["fieldname"]] = obj
        identifiers = Q(**qry["identifiers"]) & sec.rule        
        try:
            instance_ = model.objects.get(identifiers)
        except:            
            instance_ = None
        if not instance_:
            instance_ = model(**qry["defaults"])
            instance_.save()
            return instance_, True
        for key, value in qry["defaults"].items():
            setattr(instance_,key,value)            
            instance_.save()            
        return instance_, False


    def _update_or_create_row(self, qry: dict) -> list:
        model = self._get_model(qry)        
        # sec = SecurityRules(model, self.request.user, ["add","change"])     
        #    PASS SEC TO IDENTIFIERS FOR CREATION
        obj, created = self._create_or_update_single_instance(qry)                
        if created:
            msg = "NEW_TARGET_CREATED"
        else:
            msg = "TARGET_UPDATED"
        roles = self._create_collection_role(obj, qry)
        res = {
            "result": [{"status": "OK", "msg": msg, "id": obj.id, "security": roles}],
            "name": qry["name"],            
        }        
        return res

    def _update_or_create_row_and_file(self, qry: dict) -> list:
        model = self._get_model(qry)        
        # sec = SecurityRules(model, self.request.user, ["add","change"])                    
        res = []
        files = self.request.FILES.getlist("files")
        for file in files:
            qry["identifiers"][qry["file_field_name"]] = file
            qry["defaults"][qry["file_field_name"]] = file
            obj, created = self._create_or_update_single_instance(qry)
            if created:
                msg = "NEW_TARGET_CREATED"
            else:
                msg = "TARGET_UPDATED"
            roles = self._create_collection_role(obj, qry)
            res.append(
                {"filename": file.name, "status": "OK", "msg": msg, "id": obj.id, "security": roles}
            )
        res = {"result": res, "name": qry["name"]}
        return res

    def _update_or_create_row_and_file_from_path(self, qry: dict) -> list:
        model = self._get_model(qry)        
        # sec = SecurityRules(model, self.request.user, ["add","change"])                        
        res = []
        files = qry["files"]
        for file in files:
            qry["identifiers"][qry["file_field_name"]] = file
            qry["defaults"][qry["file_field_name"]] = file
            obj, created = self._create_or_update_single_instance(qry)
            file_field = getattr(obj, qry["file_field_name"])
            content, file_name = self._get_locale_file(file)
            file_field.save(file_name, ContentFile(content.encode("utf8")))
            if created:
                msg = "NEW_TARGET_CREATED"
            else:
                msg = "TARGET_UPDATED"
            roles = self._create_collection_role(obj, qry)
            res.append(
                {"filename": file_name, "status": "OK", "msg": msg, "id": obj.id, "security": roles}
            )
        res = {"result": res, "name": qry["name"]}
        return res

    def _extract_file_base(self, files: list) -> dict:
        res = {}
        regex = "__page[0-9]{4}"
        for file in files:
            _filename = os.path.basename(file)
            _filebasename = "".join(re.split(regex, _filename))
            if not _filebasename in res:
                res[_filebasename] = []
            res[_filebasename].append(file)
            res[_filebasename].sort()
        return res

    def _merge_content(self, files: list) -> dict:
        _mergedcontent = ""
        for file in files:
            content, _ = self._get_locale_file(file)
            _mergedcontent += "\n\n" + content
        return _mergedcontent

    def _create_document_item(self, name: str, project_id: int):
        qry = {
            "table": "projectdocumentcollection",
            "parents": [
                {
                    "table": "projectcollection",
                    "fieldname": "project",
                    "identifiers": {"id": project_id}
                }
            ],
            "identifiers": {"name": name},
            "defaults": {"name": name, "datapool": "IDLE"}
        }
        obj, created = self._create_or_update_single_instance(qry)
        return obj



    def _add_files_to_project(self, qry: dict) -> list:
        model = self._get_model(qry)  
        sec = SecurityRules(model, self.request.user, ["add","change"])        
        res = []
        files = qry["files"]
        _combinedfiles = self._extract_file_base(files)
        for _filebasename, _files in _combinedfiles.items():
            document = self._create_document_item(_filebasename, qry["project_id"])            
            docroles = self._create_collection_role(document, qry)
            for file in _files:
                qry["identifiers"]["document"] = document
                qry["defaults"]["document"] = document
                qry["identifiers"][qry["file_field_name"]] = file
                qry["defaults"][qry["file_field_name"]] = file                
                obj, created = self._create_or_update_single_instance(qry)
                file_field = getattr(obj, qry["file_field_name"])            
                content, file_name = self._get_locale_file(file)            
                file_field.save(file_name, ContentFile(content.encode("utf8")))
                if created:
                    msg = "NEW_TARGET_CREATED"
                else:
                    msg = "TARGET_UPDATED"
                roles = self._create_collection_role(obj, qry)
            res.append(
                {"filename": _filebasename, "status": "OK", "msg": msg, "id": document.id, "security": docroles}
            )
        res = {"result": res, "name": qry["name"]}
        return res

    def _qry_data(self, qry: dict) -> dict:
        if qry["type"] == "update":
            queryset = self._update_or_create_row(qry)
        if qry["type"] == "multi_file_upload":
            queryset = self._update_or_create_row_and_file(qry)
        if qry["type"] == "multi_file_upload_from_path":
            queryset = self._update_or_create_row_and_file_from_path(qry)
        if qry["type"] == "add_merged_files_to_project_from_path":
            queryset = self._add_files_to_project(qry)
        if qry["type"] not in [
            "update",
            "multi_file_upload",
            "multi_file_upload_from_path",
            "add_merged_files_to_project_from_path",
        ]:
            queryset = {"result": [{"error": "Unkown query type"}], "name": qry["name"]}
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
