from django.shortcuts import render, redirect
from django.urls import reverse


def index_view(request):
    """
    Shows the index.html page.
    """
    return render(request, 'index.html')

