from rest_framework import serializers
from accounting.models import Entries

class EntriesSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Entries
