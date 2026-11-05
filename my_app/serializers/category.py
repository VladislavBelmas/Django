from rest_framework import serializers
from ..models import Category


class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

    def create(self, validated_data):
        if Category.objects.filter(name=validated_data['name']).exists():
            raise serializers.ValidationError({'name': 'Name must be unique'})
        return super().create(validated_data)

    def update(self, instance, validated_data):
        new_name = validated_data.get('name')
        if new_name and new_name != instance.name:
            if Category.objects.filter(name=new_name).exists():
                raise serializers.ValidationError({'name': 'Name must be unique'})
        return super().update(instance, validated_data)
