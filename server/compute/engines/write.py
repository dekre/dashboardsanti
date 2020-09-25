from typing import List
from .utils import collector
from .core import CoreComputeEngine, WriteQuery
from compute.models import Item
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from backend.settings import MEDIA_ROOT


class WriteView(CoreComputeEngine):
    # PAULA IS THE BEST OMG I LOVE HER SO MUCH I JUST WANT TO SPEND MY LIFE WITH HER!!!!!!!
    def __call__(self, queries: str): 
        return super(WriteView, self).__call__(queries)                
        

    def _create_or_update_single_instance(self, qry: WriteQuery) -> (Item, bool,):
        """
        Saves an item with given defaul values. 
        """
        # check if item exists
        try:
            instance_ = qry.model.objects.get(**qry._identifiers)
        except (ObjectDoesNotExist, MultipleObjectsReturned):
            instance_ = None
        # if does not exist, create new
        if not instance_:
            instance_ = qry.model(**qry.defaults)
            instance_.save()
            return instance_, True
        # if does exist, update
        for key, value in qry.defaults.items():
            setattr(instance_, key, value)
            instance_.save()
        return instance_, False

    @collector('_qry_method', 'write_item')
    def _update_or_create_item(self, qry: WriteQuery) -> list:
        obj, created = self._create_or_update_single_instance(qry)
        if created:
            msg = "NEW_TARGET_CREATED"
        else:
            msg = "TARGET_UPDATED"
        res = {
            "result": [{"status": "OK", "msg": msg, "id": obj.id}],
            "name": qry.name,
        }
        return res

    @collector('_qry_method', 'write_item_file')
    def _create_or_update_item_and_file(self, qry: WriteQuery) -> list:
        res = []
        for file in qry.files:
            qry.identifiers &= Q(**{qry.file_field_name: file})
            qry.defaults.update({qry.file_field_name: file})
            obj, created = self._create_or_update_single_instance(qry)
            if created:
                msg = "NEW_TARGET_CREATED"
            else:
                msg = "TARGET_UPDATED"
            res.append(
                {"filename": file, "status": "OK", "msg": msg, "id": obj.id}
            )
        res = {"result": res, "name": qry.name}
        return res
