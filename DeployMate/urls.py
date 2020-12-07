from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from HomePage.views import homepage,build,template,publish,dashboard

#seo related
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',homepage,name='HomePage'),
    path('build/<str:build>',build,name='BuildPage'),
    path('publish/',publish,name='PublishPage'),
    path('<str:launch_id>/',template,name='TemplatePage'),
    path('<str:launch_id>/admin',dashboard,name='AdminPage'),
    path('subscribe/',template,name='SubscribePage'),
    #seo goes here
    path('robots.txt',TemplateView.as_view(template_name='SEO/robots.txt',content_type = 'text/plain')),
    path('sitemap.xml',TemplateView.as_view(template_name='SEO/sitemap.xml',content_type = 'text/xml')),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
