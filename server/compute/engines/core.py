import ast
from abc import abstractclassmethod
from .serializers import GenericResultSet
from .utils import AggregationWrapper, collector
from django.db.models.functions import *
from django.db.models import Model, Avg, Max, Min, Sum, Count, F


class BaseQuery(object):

    def __init__(self, qry: dict):
        self._qry = qry
        self.allowed_names = {
            "F": F,

        }
        self._init_qry(qry)

    def _init_qry(self, qry: dict):
        self._init_model(qry)
        self._init_identifiers(qry)
        self._init_parents(qry)
        self._init_expressions(qry)

    def _init_identifiers(self, qry: dict):
        try:
            self._identifiers = qry["identifiers"]
        except KeyError:
            print("Identifiers not specified.")

    def _init_model(self, qry: dict):
        try:
            models = apps.all_models["apidata"]
            self._model = models[qry["table"]]
        except KeyError:
            print("Table not specified.")

    def _init_parents(self, qry: dict):
        parents_ = dict()
        if "parents" in qry:
            for parent in qry["parents"]:
                obj = self._get_parent(parent)
                key = parent["fieldname"]
                self._identifiers[key] = obj
                parents_[key] = obj
        self._parents = parents_

    def _init_expressions(self, qry: dict):
        expressions_ = dict()
        if "expressions" in qry:
            for expression in qry["expressions"]:
                expressions_[expression["name"]] = self._eval(
                    expression["definition"])
        self._expressions = expressions_

    def _eval(expression):
    """Evaluate a query expression."""
    # Compile the expression
    code = compile(expression, "<string>", "eval")
    # Validate allowed names
    for name in code.co_names:
        if name not in self.allowed_names:
            raise NameError(f"The use of '{name}' is not allowed")
    return eval(code, {"__builtins__": {}}, self.allowed_names)

    def _get_parent(self, qry: dict) -> object:
        model = self._get_model(qry)
        obj = model.objects.get(**qry["identifiers"])
        return obj

    @property
    def query(self) -> dict:
        return self._qry

    @property
    def model(self) -> Model:
        return self._model

    @property
    def identifiers(self) -> dict:
        return self._identifiers

    @property
    def expressions(self) -> dict:
        return self._expressions

    @property
    def allowed_names(self):
        return {"F": F}

    @property
    def parents(self) -> dict:
        return self._parents


class ViewQuery(BaseQuery):

    def __init__(self, qry: dict):
        super(CreateQuery, self).__init__(qry)
        self.allowed_names.update({"Sum": Sum,
                                   "Avg": Avg,
                                   "Max": Max,
                                   "Min": Min,
                                   "Count": Count})
        self._init_aggregations(qry)

    def _init_aggregations(self, qry: dict):
        aggregations_ = dict()
        if "aggfields" in qry:
            for aggregation in qry["aggfields"]:
                aggregations_[aggregation["name"]] = self._eval(
                    aggregation["definition"])
        self._aggregations = aggregations_

    @property
    def aggregations(self):
        return self._aggregations


class WriteQuery(BaseQuery):

    def __init__(self, qry: dict):
        super(WriteQuery, self).__init__(qry)
        self._init_defaults(qry)
        self._init_files(qry)
        self._init_file_field_name(qry)

    def _init_defaults(self, qry: dict):
        defaults_ = self.identifiers
        if "defaults" in qry:
            defaults_ = qry["defaults"]
            defaults_.update(self.parents)
        self._defaults = defaults_

    def _init_files(self, qry: dict):
        files_ = list()
        if "files" in qry:
            files_ = qry["files"]
        self._files = files_

    def _init_file_field_name(self, qry: dict):
        file_field_name_ = str()
        if "file_field_name" in qry:
            file_field_name_ = qry["file_field_name"]
        self._file_field_name = file_field_name_

    @property
    def defaults(self) -> dict:
        return self._defaults

    @property
    def files(self) -> list:
        return self._files

    @property
    def file_field_name(self) -> str:
        return self._file_field_name


class DeleteQuery(BaseQuery):

    def __init__(self, queries: str):
        super(CreateQuery, self).__init__(queries)


class QueryFactory(object):

    def __init__(self, qry: dict):
        self.qry = qry

    def __call__(self):
        for func in dir(cls):
            if '_qry_type' in dir(getattr(cls, func)):
                if getattr(cls, func)._qry_type == self.qry["type"]:
                    func_ = getattr(cls, func)
                    return func_(self.qry)
        raise ValueError("Unkown query type provided for {}".format(qry["name"]))

    @collector("view", "_qry_type")
    def _create_qry(self, qry: dict):
        return ViewQuery(qry)

    @collector("write", "_qry_type")
    def _view_qry(self, qry: dict):
        return WriteQuery(qry)

    @collector("delete", "_qry_type")
    def _delete_qry(self, qry: dict):
        return DeleteQuery(qry)


class CoreComputeEngine(object):

    def __init__(self, queries: str = None):
        self._queries = queries

    def __call__(self):
        queries = self._cast_queries_to_dict(self.queries)
        querysets = list()
        for q in queries:
            qry = QueryFactory(q)
            querysets.append(self._qry_data(qry))
        serializer = GenericResultSet(querysets, many=True)
        return serializer.data

    @property
    def queries(self):
        return self._queries
        
    @classmethod
    def _qry_data(cls, qry: QueryFactory):
        for func in dir(cls):
            if '_qry_method' in dir(getattr(cls, func)):
                if getattr(cls, func)._qry_method == qry["method"]:
                    func_ = getattr(cls, func)
                    return func_(qry)
        raise ValueError("Unkown query method provided for {}".format(qry["name"]))        

    def _cast_queries_to_dict(self, queries: str) -> dict:
        q = ast.literal_eval(queries)
        if type(q) != dict:
            raise ValueError(
                "Parsing ERROR in queries. Converted type must be dict. You passed {}".format(
                    type(q))
            )
        return q
