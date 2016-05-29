from django.shortcuts import render

# Create your views here.


def main(request):
    ick = "this"
    return( render(request, 'hierarchy/main.html', locals() ))
