from rest_framework import routers, viewsets
from rest_framework.permissions import AllowAny

from .models import Project
from .serializers import ProjectSerializer


class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Project.objects.filter(published=True).prefetch_related('gallery')
    serializer_class = ProjectSerializer
    permission_classes = (AllowAny,)
    lookup_field = 'slug'


router = routers.DefaultRouter()
router.register('projects', ProjectViewSet, basename='api-project')