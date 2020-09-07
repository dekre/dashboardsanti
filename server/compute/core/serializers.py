from rest_framework import serializers

class GenericResultSet(serializers.Serializer):
    result = serializers.ListField()    
    name = serializers.CharField()


