from django.db.models import Sum, Avg, Max, Min, Count

qry_base_schema = {
    "model": {
        "type": "<string>",
        "is_null": False,
        "description": "Model Refernce"
    }
}

class AggregationWrapper:    

    def sum(self):
        return Sum

    def avg(self):
        return Avg
    
    def max(self):
        return Max
    
    def min(self):
        return Min

    def count(self):
        return Count


class collector:
    """
    Decorater for addig a tag to the decorated function. 
    """
    def __init__(self, func_tag: str, tag_value: str):
        self.tag_value = tag_value
        self.func_tag = func_tag
        
    def __call__(self, fn, *args, **kwargs):
        setattr(fn, self.func_tag, self.tag_value)
        return fn


