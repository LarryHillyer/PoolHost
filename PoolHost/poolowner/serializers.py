from rest_framework import serializers

from app.models import PoolGroup_Choices

class PoolGroup_Choices_Serializer(serializers.Serializer):

    name = serializers.CharField(required = True, max_length = 100)
    poolgroup_id = serializers.IntegerField(required = True)

    def create(self, validated_data):
        
        return PoolGroup_Choices.objects.create(**validated_data)

    def update(self, instance, validated_data):

        instance.name = validated_data.get('name', instance.title)
        instance.poolgroup_id = validated_data.get('poolgroup_id', instance.poolgroup_id)