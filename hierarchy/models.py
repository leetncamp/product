from django.db import models
from django.contrib.auth.models import User
from pdb import set_trace as debug

bigheaders = [u'Segment Label', u'Segment Code', u'Segment Name', u'Division Label', u'Division Code', u'Division Name', u'Business Unit Label', u'Business Unit Code', u'Business Unit Name', u'Sub-Business Unit Label', u'Sub-Business Unit Code', u'Sub-Business Unit Name', u'Product Line Group Label', u'Product Line Group Code', u'Product Line Group Name', u'Product Line Label', u'Product Line Code', u'Product Line Name', u'Igor Item Class', u'Usage', u'Igor or Sub PL', u'Igor / Sub PL Description', u'Sub-PL Label', u'Date', u'Notes1', u'Requestor', u'SAP Full Hierarchy String', u'SAP Lower Level string',]

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

class IgorItemClass(models.Model):
    name = models.CharField(max_length=1)
    description = models.CharField(max_length=64)

    def __unicode__(self):
        return(u"{0}-{1}".format(self.name, self.description))

class Usage(models.Model):
    name = models.CharField(max_length=64)

    def __unicode__(self):
        return(u"{0}".format(self.name))


segmentDict = { "GSX": "J", "CSX":"L", "MBS":"K", "FRT":"B", "MSJ":"N" }

class SubProductLine(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    description = models.CharField(max_length=30)
    igor_or_sub_pl = models.CharField(max_length=3)
    fproductline = models.ForeignKey(ProductLine)
    igorclass = models.ForeignKey(IgorItemClass, blank=True, null=True)
    usage = models.ForeignKey(Usage, blank=True, null=True)
    label = models.CharField(max_length=64, blank=True, default="")

    def save(self, *args, **kwargs):
        if not self.label:
            self.label = u"{0}- {1}".format(self.igor_or_sub_pl, self.description)
        super(SubProductLine, self).save(*args, **kwargs)

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
        result = segmentDict.get(segment.code, "#")
        result = u"".format(result)
        result += businessunit.code
        result += subbusinessunit.code
        result += productlinegroup.code
        result += productline.code
        return(segment, division, businessunit, subbusinessunit, productlinegroup, productline, result)

    def excel_row(self, ws, row):
        segment, division, businessunit, subbusinessunit, productlinegroup, productline, result = self.sapfullstring()
        column = 1
        ws.cell(row=row, column=column).value = segment.label; column += 1
        ws.cell(row=row, column=column).value = segment.code; column += 1
        ws.cell(row=row, column=column).value = segment.name; column += 1
        ws.cell(row=row, column=column).value = division.label; column += 1
        ws.cell(row=row, column=column).value = division.code; column += 1
        ws.cell(row=row, column=column).value = division.name; column += 1
        ws.cell(row=row, column=column).value = businessunit.label; column += 1
        ws.cell(row=row, column=column).value = businessunit.code; column += 1
        ws.cell(row=row, column=column).value = businessunit.name; column += 1
        ws.cell(row=row, column=column).value = subbusinessunit.label; column += 1
        ws.cell(row=row, column=column).value = subbusinessunit.code; column += 1
        ws.cell(row=row, column=column).value = subbusinessunit.name; column += 1
        ws.cell(row=row, column=column).value = productlinegroup.label; column += 1
        ws.cell(row=row, column=column).value = productlinegroup.code; column += 1
        ws.cell(row=row, column=column).value = productlinegroup.name; column += 1
        ws.cell(row=row, column=column).value = productline.label; column += 1
        ws.cell(row=row, column=column).value = productline.code; column += 1
        ws.cell(row=row, column=column).value = productline.name; column += 1
        ws.cell(row=row, column=column).value = self.igorclass.name; column += 1
        ws.cell(row=row, column=column).value = self.usage.name; column += 1
        ws.cell(row=row, column=column).value = self.igor_or_sub_pl; column += 1
        ws.cell(row=row, column=column).value = self.description; column += 1
        ws.cell(row=row, column=column).value = self.description; column += 1
        return()


class Code(models.Model):
    code = models.CharField(max_length=3)
    used = models.BooleanField(default=False, blank=True)

    def __unicode__(self):
        return(self.code)

def get_unused_code(description=None):
    code = Code.objects.filter(used=False)[0]
    return(code)
