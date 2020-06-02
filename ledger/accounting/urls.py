from django.urls import path, include
from rest_framework import routers
from accounting.views import EntriesViewSet, get_balance_by_date

router = routers.DefaultRouter()
router.register(r'entry', EntriesViewSet)

urlpatterns = [path(r'balance/<int:pk>/', get_balance_by_date)]

urlpatterns += router.urls
