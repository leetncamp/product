from django.contrib import admin

# Register your models here.


from django.contrib import admin

# Register your models here.


from hierarchy.models import *

class SegmentAdmin(admin.ModelAdmin):
    list_display = ['id', "code", "name", "label"]
    search_fields = ['id', 'code', 'name']

class DivisionAdmin(admin.ModelAdmin):
    list_display = ['id', "code", "name", "label"]
    search_fields = ['id', 'code', 'name']

class BusinessUnitAdmin(admin.ModelAdmin):
    list_display = ['id', "code", "name", "label"]
    search_fields = ['id', 'code', 'name']

class SubBusinessUnitAdmin(admin.ModelAdmin):
    list_display = ['id', "code", "name", "label"]
    search_fields = ['id', 'code', 'name']

class ProductLineGroupAdmin(admin.ModelAdmin):
    list_display = ['id', "code", "name", "label"]
    search_fields = ['id', 'code', 'name']




# Now register the new UserAdmin...
admin.site.register(Segment, SegmentAdmin)
admin.site.register(Division, DivisionAdmin)
admin.site.register(BusinessUnit, BusinessUnitAdmin)
admin.site.register(SubBusinessUnit, BusinessUnitAdmin)
admin.site.register(ProductLineGroup, ProductLineGroupAdmin)
admin.site.register(ProductLine, ProductLineGroupAdmin)
