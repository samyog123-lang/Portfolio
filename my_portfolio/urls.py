"""
URL configuration for my_portfolio project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from portfolio import views
from portfolio.api import router as api_router
from portfolio.sitemaps import BlogSitemap, ProjectSitemap, StaticPageSitemap

sitemaps = {
    'pages': StaticPageSitemap,
    'projects': ProjectSitemap,
    'journal': BlogSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('robots.txt', views.robots_txt, name='robots_txt'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
    path('', views.home, name='home'),
    path('projects/<slug:slug>/', views.project_detail, name='project_detail'),
    path('journal/', views.blog_list, name='blog_list'),
    path('journal/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('resume/', views.resume_download, name='resume_download'),
    path('api/', include(api_router.urls)),
    path('api/chat/', views.chat, name='chat'),
    path('api/contact/', views.submit_contact, name='submit_contact'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler403 = 'portfolio.views.permission_denied'
handler404 = 'portfolio.views.page_not_found'
handler500 = 'portfolio.views.server_error'
