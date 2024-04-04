from rest_framework import serializers
from . import models


# class TodoSerializer(serializers.Serializer):
#     id=serializers.IntegerField(read_only=True)
#     title=serializers.CharField(max_length=200)
#     status=serializers.ChoiceField(choices=models.status_choices,default='P')
#     priority=serializers.ChoiceField(choices=models.priority_choices,default='1')
#     date=serializers.DateTimeField(read_only=True, format=r"%Y-%m-%d")
#     user=serializers.

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TODO
        fields = ['id', 'title', 'status', 'priority',]

    def create(self, validated_data):
        # user=validated_data['user']
        # print(user)
        print(validated_data)
        return models.TODO.objects.create(**validated_data)
