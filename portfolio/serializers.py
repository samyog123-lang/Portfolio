from rest_framework import serializers

from .models import Project, ProjectImage


class ProjectImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectImage
        fields = ('image', 'alt_text', 'display_order')


class ProjectSerializer(serializers.ModelSerializer):
    gallery = ProjectImageSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = (
            'title',
            'slug',
            'summary',
            'description',
            'category',
            'thumbnail',
            'image_alt',
            'technologies',
            'github_url',
            'live_url',
            'technical_highlights',
            'featured',
            'project_date',
            'gallery',
        )