from django.db import models

# Create your models here.

class Parent(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    code = models.CharField(max_length=3)
    label = models.CharField(max_length=64, blank=True, default="")
    name = models.CharField(max_length=30)

    def __unicode__(self):
        return(u"{0}- {1}".format(self.code, self.name))

    def save(self, *args, **kwargs):
        if not self.label:
            self.label = u"{0}- {1}".format(self.code, self.name)
        super(Parent, self).save(*args, **kwargs)

class Segment(Parent):
    pass

class Division(Parent):
    pass

class BusinessUnit(Parent):
    pass

class SubBusinessUnit(Parent):
    pass

class ProductLineGroup(Parent):
    pass

class ProductLine(Parent):
    pass

class SubProductLine(Parent):
    pass

class IgorItemClass(models.Model):
    name = models.CharField(max_length=1)
    description = models.CharField(max_length=64)

    def __unicode__(self):
        return(u"{0}-{1}".format(self.name, self.description))

class ProductHierarchy(models.Model):
    date = models.DateTimeField()
