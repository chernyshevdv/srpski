from django.http import HttpRequest
from django.shortcuts import render, redirect


def cases(request: HttpRequest):
    return render(request, "theory_cases.html")