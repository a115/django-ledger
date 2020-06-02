from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from django.shortcuts import render
from accounting.models import Account, Entries, AccountBalance
from accounting.serializers import EntriesSerializer, AccountBalanceSerializer

 # Get, Create, Update, Delete a Entry
class EntriesViewSet(viewsets.ModelViewSet):
    queryset = Entries.objects.all()
    serializer_class = EntriesSerializer


@api_view(['POST'])
def get_balance_by_date(request, pk):
    """
    Given a date get the account_balance.
    """
    try:
        account = Account.objects.get(pk=pk)
    except Account.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    date = request.data['date']
    balance = AccountBalance.objects.filter(account=account, timestamp=date)
    serialize_balance = AccountBalanceSerializer(balance)
    return Response(serialize_balance.data)
