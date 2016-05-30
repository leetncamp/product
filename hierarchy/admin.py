from django.contrib import admin
from hierarchy.models import *
from hierarchy.models import SubProductLine

class SegmentAdmin(admin.ModelAdmin):
    list_display = ['id', "code", "name", "label"]
    search_fields = ['id', 'code', 'name']

class DivisionAdmin(admin.ModelAdmin):
    list_display = ['id', "code", "name", "label", 'fsegment']
    search_fields = ['id', 'code', 'name']

class BusinessUnitAdmin(admin.ModelAdmin):
    list_display = ['id', "code", "name", "label",  "fdivision"]
    search_fields = ['id', 'code', 'name']

class SubBusinessUnitAdmin(admin.ModelAdmin):
    list_display = ['id', "code", "name", "label", "fbusinessunit"]
    search_fields = ['id', 'code', 'name']

class ProductLineGroupAdmin(admin.ModelAdmin):
    list_display = ['id', "code", "name", "label", "fsubbusinessunit"]
    search_fields = ['id', 'code', 'name']

class ProductLineAdmin(admin.ModelAdmin):
    list_display = ['id', "code", "name", "label", "fproductlinegroup"]
    search_fields = ['id', 'code', 'name']


class IgorItemClassAdmin(admin.ModelAdmin):
    list_display = ['id', "name", "description"]
    search_fields = ['id', 'description', 'name']

class UsageAdmin(admin.ModelAdmin):
    search_fields = ['name']

class SubProductLineAdmin(admin.ModelAdmin):
    search_fields = ['igor_or_sub_pl', 'description']
    list_display = ['id', 'description', 'igor_or_sub_pl', 'fproductline', lambda x:x.sapfullstring() ]



# Now register the new UserAdmin...
admin.site.register(Segment, SegmentAdmin)
admin.site.register(Division, DivisionAdmin)
admin.site.register(BusinessUnit, BusinessUnitAdmin)
admin.site.register(SubBusinessUnit, SubBusinessUnitAdmin)
admin.site.register(ProductLineGroup, ProductLineGroupAdmin)
admin.site.register(ProductLine, ProductLineAdmin)
admin.site.register(IgorItemClass, IgorItemClassAdmin)
admin.site.register(Usage, UsageAdmin)
admin.site.register(SubProductLine, SubProductLineAdmin)
