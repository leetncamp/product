from django.conf.urls import patterns, include, url
from django.contrib import admin
from hierarchy.views import *

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^uploadproducthierarchy$', import_product_hierarchy, name="import_product_hierarchy"),
    url(r'^requestnew$', requestnew, name="requestnew"),
)
