from django.conf.urls import include, url
from django.contrib import admin
from hierarchy.views import *

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^uploadproducthierarchy$', import_product_hierarchy, name="import_product_hierarchy"),
    url(r'^new$', new, name="new"),
    url(r'^replacecodes', replacecodes, name="replacecodes"),
    url(r'^update_code', update_code, name="update_code"),
    url(r'^$', new),
    url(r'^downloadproducthierarchy/{0,1}$', download_product_hierarchy, name="download_product_hierarchy" ),
    url(r'^aloha$', aloha, name="aloha"),
    ]
