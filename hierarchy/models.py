from django.db import models
from django.contrib.auth.models import User
from pdb import set_trace as debug


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
    fsegment = models.ForeignKey(Segment)

class BusinessUnit(Parent):
    fdivision = models.ForeignKey(Division)

class SubBusinessUnit(Parent):
    fbusinessunit = models.ForeignKey(BusinessUnit)

class ProductLineGroup(Parent):
    fsubbusinessunit = models.ForeignKey(SubBusinessUnit)

class ProductLine(Parent):
    fproductlinegroup = models.ForeignKey(ProductLineGroup)

class SubProductLine(models.Model):
    segmentDict = { "GSX": "J", "CSX":"L", "MBS":"K", "FRT":"B", "MSJ":"N" }
    description = models.CharField(max_length=30)
    igor_or_sub_pl = models.CharField(max_length=3)
    fproductline = models.ForeignKey(ProductLine)


    def __unicode__(self):
        return(u"{0}- {1}".format(self.igor_or_sub_pl, self.description))

    def sapfullstring(self):
        productline = self.fproductline
        productlinegroup = productline.fproductlinegroup
        subbusinessunit =  productlinegroup.fsubbusinessunit
        businessunit = subbusinessunit.fbusinessunit
        division = businessunit.fdivision
        segment = division.fsegment

        #=IF($B2="GSX","J",IF($B2="CSX","L",IF($B2="MBS","K",IF($B2="FRT","B",IF($B2="MSJ","N","#")))))&$H2&$K2&$N2&$Q2&$S2&$U2
        result = self.segmentDict.get(segment.code, "#")
        result = u"".format(result)
        result += businessunit.code
        result += subbusinessunit.code
        result += productlinegroup.code
        result += productline.code
        return(result)


class IgorItemClass(models.Model):
    name = models.CharField(max_length=1)
    description = models.CharField(max_length=64)

    def __unicode__(self):
        return(u"{0}-{1}".format(self.name, self.description))

class Usage(models.Model):
    name = models.CharField(max_length=64)

    def __unicode__(self):
        return(u"{0}".format(self.name))

class ProductHierarchy(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    subpl = models.ForeignKey(SubProductLine, blank=True, null=True)
    pl = models.ForeignKey(ProductLine)
    igorclass = models.ForeignKey(IgorItemClass, blank=True, null=True)
    usage = models.ForeignKey(Usage, blank=True, null=True)

class Code(models.Model):
    code = models.CharField(max_length=3)
    used = models.BooleanField(default=False, blank=True)

    def __unicode__(self):
        return(self.code)
