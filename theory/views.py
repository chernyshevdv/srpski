from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect


def theory_sections(request: HttpRequest, section: str) -> HttpResponse:
    SECTIONS = ["cases", "cases_pronouns"]
    return render(request, f"theory_{section}.html", {"sections": SECTIONS})