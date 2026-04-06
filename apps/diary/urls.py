from rest_framework.routers import DefaultRouter
from .views import DiaryEntryViewSet

router = DefaultRouter()
router.register(r'', DiaryEntryViewSet, basename='diary')

urlpatterns = router.urls