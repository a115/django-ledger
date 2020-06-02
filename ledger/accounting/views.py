from django.shortcuts import render
from accounting.models import Entries
from accounting.serializers import EntriesSerializer
# Create your views here.
#view for adding entries, and a view for showing the balance on an account at a given date

from rest_framework import viewsets

class EntriesViewSet(viewsets.ModelViewSet):
    queryset = Entries.objects.all()
    serializer_class = EntriesSerializer
