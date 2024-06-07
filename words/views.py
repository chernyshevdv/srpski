from django.http import HttpRequest, HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, get_list_or_404
from icecream import ic
import random

from .models import Word, WordList

def list_wordlists(request: HttpRequest):
    rows = WordList.objects.all().order_by('title')

    return render(request, "words_lists_list.html", {'rows': rows})


def guess_words_in_list(request: HttpRequest, id: int):
    lst = get_object_or_404(WordList, pk=id)
    ic(lst)
    nav_lists = WordList.objects.all()

    words = request.session.get('words', lst.word_set.all())
    ic(words)
    count = len(words)
    position = random.randrange(count)
    word_to_guess = words[position]
    ic(word_to_guess)

    return render(request, "words_guess_word.html", {'list': lst, 'lists': nav_lists, 'word': word_to_guess})
