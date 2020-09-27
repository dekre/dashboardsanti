import ast
from abc import abstractclassmethod
from compute.serializers import GenericResultSet
from .utils import AggregationWrapper, collector
from django.apps import apps
from django.db.models import Model, Avg, Max, Min, Sum, Count, F, Q


class BaseQuery(object):

    def __init__(self, qry: dict):
        self._qry = qry
        self._allowed_names = {
            "F": F,
            "Q": Q
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
            models = apps.all_models["compute"]
            self._model = models[qry["model"]]
        except KeyError:
            print("Model not specified.")

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

    def _eval(self, expression):
        """Evaluate a query expression."""
        # Compile the expression
        code = compile(expression, "<string>", "eval")
        # Validate allowed names
        for name in code.co_names:
            if name not in self.allowed_names:
                raise NameError(f"The use of '{name}' is not allowed")
        return eval(code, {"__builtins__": {}}, self.allowed_names)

    def _get_parent(self, qry: dict) -> object:
        obj = self.model.objects.get(**qry["identifiers"])
        return obj

    @property
    def query(self) -> dict:
        return self._qry

    @property
    def method(self) -> str:
        return self._qry["method"]
    
    @property
    def name(self) -> str:
        return self._qry["name"]

    @property
    def model(self) -> Model:
        return self._model

    @property
    def identifiers(self) -> Q:
        return Q(**self._identifiers) & Q(**self.parents)

    @property
    def expressions(self) -> dict:
        return self._expressions

    @property
    def allowed_names(self):
        return self._allowed_names

    @property
    def parents(self) -> dict:
        return self._parents


class ViewQuery(BaseQuery):

    def __init__(self, qry: dict):
        super(ViewQuery, self).__init__(qry)
        self._init_allowed_names()
        self._init_aggregations(qry)
        self._init_categories(qry)
        self._init_orderby(qry)
        self._init_top_nrows(qry)

    def _init_allowed_names(self):
        self._allowed_names.update(
            {
                "Sum": Sum,
                "Avg": Avg,
                "Max": Max,
                "Min": Min,
                "Count": Count
            }
        )

    def _init_aggregations(self, qry: dict):
        aggregations_ = dict()
        if "aggfields" in qry:
            for aggregation in qry["aggfields"]:
                aggregations_[aggregation["name"]] = self._eval(
                    aggregation["definition"])
        self._aggregations = aggregations_    

    def _init_categories(self, qry: dict):
        categories_ = tuple()
        if "categories" in qry:
            categories_ = tuple(qry["categories"])
        self._categories = categories_

    def _init_orderby(self, qry: dict):
        orderby_ = tuple()
        if "orderby" in qry:
            orderby_ = tuple(qry["orderby"])
        self._orderby = orderby_

    def _init_top_nrows(self, qry: dict):
        nrows_ = None
        if "top" in qry:
            nrows_ = qry["top"]
        self._top_nrows = nrows_

    @property
    def aggregations(self) -> dict:
        return self._aggregations    

    @property
    def categories(self) -> tuple:
        return self._categories

    @property
    def orderby(self) -> tuple:
        return self._orderby

    @property
    def top_nrows(self) -> int:
        return self._top_nrows


class WriteQuery(BaseQuery):

    def __init__(self, qry: dict):
        super(WriteQuery, self).__init__(qry)
        self._init_defaults(qry)
        self._init_files(qry)
        self._init_file_field_name(qry)

    def _init_defaults(self, qry: dict):
        defaults_ = {}        
        if "defaults" in qry:
            defaults_.update(qry["defaults"])        
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
        super(DeleteQuery, self).__init__(queries)


class QueryFactory(object):

    def __call__(self, qry: dict):
        for func in dir(self):        
            if '_qry_type' in dir(getattr(self, func)):                
                if getattr(self, func)._qry_type == qry["type"]:
                    func_ = getattr(self, func)
                    return func_(qry)
        raise ValueError(
            "Unkown query type provided for {}".format(qry["name"]))

    @collector("_qry_type", "view")
    def _view_qry(self, qry: dict):
        return ViewQuery(qry)

    @collector("_qry_type", "write")
    def _write_qry(self, qry: dict):
        return WriteQuery(qry)

    @collector("_qry_type", "delete")
    def _delete_qry(self, qry: dict):
        return DeleteQuery(qry)


class CoreComputeEngine(object):
    
    def __call__(self, queries: str = None) -> list:
        queries = self._cast_queries_to_dict(queries)        
        querysets = list()
        for q in queries:
            Query_ = QueryFactory()
            qry = Query_(q) 
            querysets.append(self._qry_data(qry))
        serializer = GenericResultSet(querysets, many=True)
        return serializer.data

    def _qry_data(self, qry: QueryFactory):
        for func in dir(self):
            if '_qry_method' in dir(getattr(self, func)):
                if getattr(self, func)._qry_method == qry.method:
                    func_ = getattr(self, func)
                    return func_(qry)
        raise ValueError(
            "Unkown query method provided for {}".format(qry.method))

    def _cast_queries_to_dict(self, queries: str) -> dict:
        q = ast.literal_eval(queries)
        if type(q) != list:
            raise ValueError(
                "Parsing ERROR in queries. Converted type must be dict. You passed {}".format(
                    type(q))
            )
        return q
