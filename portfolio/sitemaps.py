from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import BlogPost, Project


class StaticPageSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.8

    def items(self):
        return ('home', 'blog_list')

    def location(self, item):
        return reverse(item)


class ProjectSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.7

    def items(self):
        return Project.objects.filter(published=True)


class BlogSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.6

    def items(self):
        return BlogPost.objects.filter(published=True)