from rest_framework import serializers
from accounting.models import Entries, AccountBalance


class EntriesSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Entries


class AccountBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = AccountBalance
