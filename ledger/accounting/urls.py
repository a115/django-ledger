from django.urls import path, include
from rest_framework import routers
from accounting.views import EntriesViewSet

router = routers.DefaultRouter()
router.register(r'entry', EntriesViewSet)

urlpatterns = router.urls
