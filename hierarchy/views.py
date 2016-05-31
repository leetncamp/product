from django.shortcuts import render
from django import forms
from openpyxl import load_workbook, Workbook
from hierarchy.models import *
import traceback
from django.db import IntegrityError
from django import forms
from tempfile import NamedTemporaryFile
from django.http import HttpResponse
import os, sys
from django.contrib import messages


class SubProductForm(forms.Form):
    subproduct = forms.FileField()

class ProductForm(forms.Form):
    product = forms.FileField()

def new(request):
    subproductform = SubProductForm()
    productform = ProductForm()
    if request.method == "POST":
        if request.POST.get("select", "") == "subproduct":
            wb = load_workbook(request.FILES['subproduct'])
            ws = wb.active
            headers = [cell.value for cell in ws.rows[0] ]
            subprods=[]
            for row in ws.rows[1:]:
                rowDict = {}
                for cellnum in range(len(row) + 1):
                    try:
                        cell = row[cellnum]
                        rowDict[headers[cellnum]] = cell.value
                    except IndexError:
                        pass
                productline = ProductLine.objects.get(code=rowDict.get("Existing Product Line Code"))
                code = get_unused_code()
                description = rowDict.get("Igor / Sub PL Description", "")
                usage = rowDict.get("Usage")
                if usage:
                    usage = Usage.objects.get(name=usage)
                igoritemclass = rowDict.get("Igor Item Class", None)
                if igoritemclass:
                    igoritemclass = IgorItemClass.objects.get(name=igoritemclass)
                subproductline, created = SubProductLine.objects.get_or_create(fproductline=productline,
                    igor_or_sub_pl=code.code, description=description, igorclass=igoritemclass, usage=usage)
                if created:
                    subproductline.save()
                    subprods.append(subproductline)
                    code.used = True
                    code.save()


            wb = Workbook()
            ws = wb.active
            count=1
            tmp = NamedTemporaryFile(suffix=".xlsx")
            for header in bigheaders:
                ws.cell(row=1, column=count).value= header
                count += 1
            count = 2

            for subprod in subprods:
                subprod.excel_row(ws, count)
                count += 1
            wb.save(tmp)
            tmp.flush()
            tmp.seek(0)
            response = HttpResponse(content_type='application/xlsx')
            response['Content-Disposition'] = 'attachment; filename="{0}"'.format(os.path.basename(tmp.name))
            response.write(tmp.read())
            return(response)
    newClass = "active"
    return(render(request, "hierarchy/new.html", locals()))

class UploadFileForm(forms.Form):
    file = forms.FileField()

def import_product_hierarchy(request):
    uploadClass = "active"
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

                    igorclassStr = rowDict.get("Igor Item Class")
                    if igorclassStr:
                        igorclass = IgorItemClass.objects.get(name=igorclassStr)
                    else:
                        igorclass = None

                    usageStr = rowDict.get("Usage")
                    if usageStr:
                        usage = Usage.objects.get(name=usageStr)
                    else:
                        usage = None

                    if rowDict["Igor or Sub PL"]:
                        subproductline, created = SubProductLine.objects.get_or_create(igor_or_sub_pl=rowDict["Igor or Sub PL"], \
                            description=rowDict['Igor / Sub PL Description'], fproductline=productline, usage=usage, igorclass=igorclass)
                        if created:
                            subproductline.save()
                    else:
                        subproductline = None

                    print row[0].row
                except Exception as e:
                    print traceback.format_exc()
                    print("Error on row {0}".format(row[0].row))
                    debug()



    return( render(request, 'hierarchy/import_product_hierarchy.html', locals() ))

def download_product_hierarchy(request):
    productlines = ProductLine.objects.all().order_by("id")
    wb = Workbook()
    ws = wb.active
    column = 1
    for header in bigheaders:
        ws.cell(row=1, column=column).value = header
        column += 1
    tmp = NamedTemporaryFile(suffix=".xlsx")
    row = 2
    for pl in productlines:
        spls = pl.subproductline_set.all()
        if spls:
            for spl in spls:
                spl.excel_row(ws, row)
                row += 1
        else:
            pl.excel_row(ws, row)
            row += 1
        print("."),
        sys.stdout.flush()
    wb.save(tmp)
    tmp.seek(0)
    response = HttpResponse(content_type='application/xlsx')
    response['Content-Disposition'] = 'attachment; filename="{0}"'.format(os.path.basename(tmp.name))
    response.write(tmp.read())
    return(response)

def aloha(request):

    """Ajax calls to save edited documents"""

    data = {"message":"Unknown Error"}

    if request.is_ajax():
        if request.user.is_superuser or userCanEdit:
            site = get_current_site(request)
            userCanEdit = request.user.groups.filter(name="CanEdit").exists()
            contentId = request.POST.get(u'contentId')
            content = request.POST.get(u'content')
            docModelStr = contentId.split("-")[0]
            docId = contentId.split("-")[1]
            if contentId and content and docModelStr and docId:

                """write this document to it's html file on disk, and eventually put it back to the dropbox folder."""
                #First do a security check on the docModelStr to make sure it's a model name before evaling it.
                if not docModelStr in modelNames:
                    return(JsonResponse({"message":"bad model"}))
                #Currently we only accept HTMLFile objects so let's further restrict.s
                if not docModelStr == "HTMLFile":
                    return(JsonResponse({"message":"bad model"}))
                docModel = eval(docModelStr)
                try:
                    doc = docModel.objects.get(pk=docId)
                except docModel.DoesNotExist:
                    return({"message":"Document not found. Save aborted."})

                open(doc.get_absolute_filepath(), "wb").write(content.encode('utf-8'))
                try:
                    doc.save()
                except Exception as e:
                    log.warning(traceback.format_exc)
                log.info(u"User {0} updated {1} with id {2}. Ondisk it is {3}".format(request.user, docModelStr, doc.id, doc.get_absolute_filepath()))
                data['message'] = u"{0} saved.".format(doc.filename)
                data = {}  #Don't pop up any window.
            else:
                data = {"message":"missing a required component. These are required: contentId and content and \
                    docModelStr and docId "}
    else:
        data = {"message":"API"}
    return(JsonResponse(data))
