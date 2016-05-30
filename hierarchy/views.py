from django.shortcuts import render
from django import forms
from openpyxl import load_workbook
from hierarchy.models import *
import traceback
from django.db import IntegrityError


def main(request):
    ick = "this"
    return( render(request, 'hierarchy/main.html', locals() ))





class UploadFileForm(forms.Form):
    file = forms.FileField()

def import_product_hierarchy(request):
    form = UploadFileForm()
    if request.method == "POST":
        if request.FILES:
            print("Loading spreadsheet")
            wb = load_workbook(request.FILES['file'])
            #Get the first sheet
            ws = wb.active
            headers = [cell.value for cell in ws.rows[0] ]
            print("Parsing rows")
            for row in ws.rows[1:]:
                try:
                    rowDict = {}
                    for cellnum in range(len(row) + 1):
                        try:
                            cell = row[cellnum]
                            rowDict[headers[cellnum]] = cell.value
                        except IndexError:
                            pass
                    segment, created = Segment.objects.get_or_create(name=rowDict["Segment Name"], code=rowDict['Segment Code'])
                    if created:
                        segment.save()
                    division, created = Division.objects.get_or_create(name=rowDict["Division Name"], code=rowDict['Division Code'], fsegment=segment)
                    if created:
                        division.save()
                    businessunit, created = BusinessUnit.objects.get_or_create(name=rowDict["Business Unit Name"], code=rowDict['Business Unit Code'], fdivision = division)
                    if created:
                        businessunit.save()
                    subbusinessunit, created = SubBusinessUnit.objects.get_or_create(name=rowDict["Sub-Business Unit Name"], code=rowDict['Sub-Business Unit Code'], fbusinessunit = businessunit)
                    if created:
                        subbusinessunit.save()
                    productlinegroup, created = ProductLineGroup.objects.get_or_create(name=rowDict["Product Line Group Name"], code=rowDict['Product Line Group Code'], fsubbusinessunit = subbusinessunit)
                    if created:
                        productlinegroup.save()
                    productline, created = ProductLine.objects.get_or_create(name=rowDict["Product Line Name"], code=rowDict['Product Line Code'], fproductlinegroup = productlinegroup)
                    if created:
                        productline.save()
                    usage, created = Usage.objects.get_or_create(name=rowDict["Usage"])

                    if created:
                        usage.save()

                    if rowDict["Igor or Sub PL"]:
                        subproductline, created = SubProductLine.objects.get_or_create(igor_or_sub_pl=rowDict["Igor or Sub PL"], description=rowDict['Igor / Sub PL Description'], fproductline=productline)
                        if created:
                            subproductline.save()
                    print row[0].row
                except Exception as e:
                    print traceback.format_exc()
                    print("Error on row {0}".format(row[0].row))
                    debug()



    return( render(request, 'hierarchy/import_product_hierarchy.html', locals() ))
