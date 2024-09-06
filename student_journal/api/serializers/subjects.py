from rest_framework import serializers
from api.models import Subject

class ListSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name', 'description']
        
class PostSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['name', 'description']
        
    def validate_name(self, value):
        if Subject.objects.filter(name=value).exclude(id=self.instance.id if self.instance else None).exists():
            raise serializers.ValidationError("A subject with this name already exists.")
        return value
        
class PatchSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['name', 'description']
        
    def validate_name(self, value):
        if Subject.objects.filter(name=value).exclude(id=self.instance.id if self.instance else None).exists():
            raise serializers.ValidationError("A subject with this name already exists.")
        return value