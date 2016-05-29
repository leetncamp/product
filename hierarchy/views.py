from django.shortcuts import render
from pdb import set_trace as debug
from django import forms
from openpyxl import load_workbook
from hierarchy.models import *
import traceback


def main(request):
    ick = "this"
    return( render(request, 'hierarchy/main.html', locals() ))





class UploadFileForm(forms.Form):
    file = forms.FileField()

def import_product_hierarchy(request):
    form = UploadFileForm()
    if request.method == "POST":
        if request.FILES:
            wb = load_workbook(request.FILES['file'])
            #Get the first sheet
            ws = wb.active
            headers = [cell.value for cell in ws.rows[0] ]
            #Create segments
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
                    division, created = Division.objects.get_or_create(name=rowDict["Division Name"], code=rowDict['Division Code'])
                    if created:
                        division.save()
                    businessunit, created = BusinessUnit.objects.get_or_create(name=rowDict["Business Unit Name"], code=rowDict['Business Unit Code'])
                    if created:
                        businessunit.save()
                    subbusinessunit, created = SubBusinessUnit.objects.get_or_create(name=rowDict["Sub-Business Unit Name"], code=rowDict['Sub-Business Unit Code'])
                    if created:
                        subbusinessunit.save()
                    obj, created = ProductLineGroup.objects.get_or_create(name=rowDict["Product Line Group Name"], code=rowDict['Product Line Group Code'])
                    if created:
                        obj.save()
                    obj, created = ProductLine.objects.get_or_create(name=rowDict["Product Line Name"], code=rowDict['Product Line Code'])
                    if created:
                        obj.save()
                except Exception as e:
                    print traceback.format_exc()
                    debug()



    return( render(request, 'hierarchy/import_product_hierarchy.html', locals() ))
