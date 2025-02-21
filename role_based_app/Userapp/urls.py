from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MemberViewSet, RoleViewSet, RightViewSet

router = DefaultRouter()
router.register('members', MemberViewSet)
router.register('roles', RoleViewSet)
router.register('rights', RightViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
