from django.db import models
from django.contrib.auth.models import User
from pdb import set_trace as debug
import datetime
stop=debug

class DescriptionTooLong(Exception): pass

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
        msg=u""
        self.name = unicode(self.name).upper()
        if len(self.name) > 30:
            msg = u"Name too long: {0}".format(self.name)
            self.name = self.name[:30]
        if not self.label:
            self.label = u"{0}- {1}".format(self.code, self.name)
        super(Parent, self).save(*args, **kwargs)
        return(msg)

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

    def get_hierarchy(self):
        productlinegroup = self.fproductlinegroup
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
        return(segment, division, businessunit, subbusinessunit, productlinegroup, result)

    def sapfullstring(self):
        #I don't think this method is needed. You don't calculate sapfullstring on produclines; only on subproductlines
        segment, division, businessunit, subbusinessunit, productlinegroup, result, lowersapresult = self.get_hierarchy()
        return(result)

    def excel_row(self, ws, row):
        segment, division, businessunit, subbusinessunit, productlinegroup, result, lowersapresult = self.get_hierarchy()
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
        ws.cell(row=row, column=column).value = self.label; column += 1
        ws.cell(row=row, column=column).value = self.code; column += 1
        ws.cell(row=row, column=column).value = self.name; column += 1
        #if self.igorclass:
        #    ws.cell(row=row, column=column).value = self.igorclass.name; column += 1
        #else:
        #    column += 1
        ws.cell(row=row, column=column).value = "-"; column += 1 #Igorlass column
        ws.cell(row=row, column=column).value = "-"; column += 1 #Usage column
        ws.cell(row=row, column=column).value = "-"; column += 1
        ws.cell(row=row, column=column).value = "-"; column += 1
        ws.cell(row=row, column=column).value = "-"; column += 1
        return()



class IgorItemClass(models.Model):
    name = models.CharField(max_length=1)
    description = models.CharField(max_length=64)

    def __unicode__(self):
        return(u"{0}-{1}".format(self.name, self.description))

class Usage(models.Model):
    name = models.CharField(max_length=64)

    def __unicode__(self):
        return(u"{0}".format(self.name))


segmentDict = { "GSX": "J", "CSX":"L", "MBS":"K", "FRT":"B", "MSJ":"N", "ZZZ":"X" }



class SubProductLine(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    description = models.CharField(max_length=30)
    #Note that is is not a  ForeignKey for code for some reason.
    igor_or_sub_pl = models.CharField(max_length=3)
    fproductline = models.ForeignKey(ProductLine)
    igorclass = models.ForeignKey(IgorItemClass, blank=True, null=True)
    usage = models.ForeignKey(Usage, blank=True, null=True)
    label = models.CharField(max_length=64, blank=True, default="")

    def save(self, *args, **kwargs):
        msg = u""
        self.description = unicode(self.description).upper()

        if len(self.description) > 30:
            self.description = self.description[:30]
            msg = u"SubProductLine description too long"

        if not self.label:
            self.label = u"{0}- {1}".format(self.igor_or_sub_pl, self.description)
        super(SubProductLine, self).save(*args, **kwargs)
        return(msg)

    def __unicode__(self):
        return(u"{0}- {1}".format(self.igor_or_sub_pl, self.description))

    def get_hierarchy(self):
        productline = self.fproductline
        productlinegroup = productline.fproductlinegroup
        subbusinessunit =  productlinegroup.fsubbusinessunit
        businessunit = subbusinessunit.fbusinessunit
        division = businessunit.fdivision
        segment = division.fsegment
        igorclass = self.igorclass.name if self.igorclass else u""

        #=IF($B2="GSX","J",IF($B2="CSX","L",IF($B2="MBS","K",IF($B2="FRT","B",IF($B2="MSJ","N","#")))))&$H2&$K2&$N2&$Q2&$S2&$U2
        #Lower sap string
        #=IF($B2="GSX","J",IF($B2="CSX","L",IF($B2="MBS","K",IF($B2="FRT","B",IF($B2="MSJ","N","#")))))&$H2&$K2&$N2


        result = segmentDict.get(segment.code, "#")
        result += str(businessunit.code)
        result += str(subbusinessunit.code)
        result += str(productlinegroup.code)
        lowersapresult = result
        result += str(productline.code)
        result += igorclass
        result += self.igor_or_sub_pl

        return(segment, division, businessunit, subbusinessunit, productlinegroup, productline, result, lowersapresult)

    def sapfullstring(self):
        segment, division, businessunit, subbusinessunit, productlinegroup, productline, result, lowersapresult = self.get_hierarchy()
        return(result)

    def saplowerstring(self):
        segment, division, businessunit, subbusinessunit, productlinegroup, productline, result, lowersapresult = self.get_hierarchy()
        return(saplowerresult)



    def excel_row(self, ws, row):
        segment, division, businessunit, subbusinessunit, productlinegroup, productline, result, lowersapresult = self.get_hierarchy()
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
        ws.cell(row=row, column=column).value = productline.code.code; column += 1
        ws.cell(row=row, column=column).value = productline.name; column += 1
        if self.igorclass:
            ws.cell(row=row, column=column).value = self.igorclass.name; column += 1
        else:
            column += 1
        ws.cell(row=row, column=column).value = self.usage.name; column += 1
        ws.cell(row=row, column=column).value = self.igor_or_sub_pl; column += 1
        ws.cell(row=row, column=column).value = self.description; column += 1
        ws.cell(row=row, column=column).value = self.label; column += 1
        column += 3

        #SAP Full Hierarchy String
        #SAP Lower Level string

        if self.igorclass:
            ws.cell(row=row, column=column).value = result; column += 1
            ws.cell(row=row, column=column).value = lowersapresult; column += 1

        return()


class Code(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    code = models.CharField(max_length=3)
    used = models.BooleanField(default=False, blank=True)

    def use(self, newcodes):
        if not self.used:
            self.used = True
            self.save()
            print(u"{0} is  marked as used".format(self.code))
            description = u""
            try:
                pl = ProductLine.objects.get(code=self)
                description = u"{0}".format(pl.label)
            except ProductLine.DoesNotExist:
                pass
            try:
                subPL = SubProductLine.objects.get(igor_or_sub_pl=self.code)
                description = u"{0}".format(subPL.description)
            except SubProductLine.DoesNotExist:
                pass
            date = unicode(datetime.datetime.now().date())
            new3digitcode = [self.code, description, date]
            newcodes.append(new3digitcode)



    def __unicode__(self):
        return(self.code)


def get_unused_code():
    code = Code.objects.filter(used=False)[0]
    return(code)
