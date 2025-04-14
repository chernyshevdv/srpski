from django.contrib import messages
from django.http import HttpRequest, HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from icecream import ic
import random
from thefuzz import fuzz
from .forms import GuessForm

from .models import Word, WordList

def list_wordlists(request: HttpRequest):
    lst = WordList.objects.first()

    return redirect("guess_words_in_list", id=lst.id)


def guess_words_in_list(request: HttpRequest, id: int):
    lst = get_object_or_404(WordList, pk=id)
    session_list_id = request.session.get('list_id', 0)
    tries = request.session.get('tries', 0)
    if session_list_id != id:
        request.session['list_id'] = id
        request.session['words'] = list(lst.word_set.all().values())
        tries = 0
    
    # By this row, we should have session['list_id] and session['words']
    words = request.session.get('words')
    # ic(lst, words)
    nav_lists = WordList.objects.all().order_by("title")
    
    if request.method == "POST":
        tries += 1
        form_post = GuessForm(request.POST)
        ic(form_post)
        word_id = int(form_post['word_id'].value())
        word = get_object_or_404(Word, id=word_id)
        guess = form_post['guess'].value()
        ic(word.drugi, guess)
        if guess == "noidea":
            msg = f"{word.srpski} = {word.drugi}"
            cls = messages.ERROR
            tags = "alert alert-warning"
        else:
            ratio = fuzz.ratio(word.drugi, guess)
            if ratio > 70:
                msg = f"Tako je! {word.srpski} = {word.drugi}"
                cls = messages.INFO
                tags = "alert alert-success"
                # remove the word from session['words']
                ic(f"Trying to remove word {word} with id {word_id}...")
                for i,x in enumerate(words):
                    ic(f"Is {x['id']} the right id {word_id}?")
                    if x['id'] == word_id:
                        ic("Yup! Removing!")
                        del words[i]
                    else:
                        ic("no", x['id'], word_id)
            else:
                msg = f"Nije tačno... Pravo je: {word.drugi}"
                cls = messages.ERROR
                tags = "alert alert-warning"
        
        messages.add_message(request, level=cls, message=msg, extra_tags=tags)

    
    count_left = len(words)
    count_total = len(lst.word_set.all())
    if count_left == 0:
        success_rate = 100 * count_total / tries 
        messages.add_message(request, level=messages.INFO, 
                             message=f"Well done! You have guessed all the words. Success rate is {success_rate:.0f}%! Try another list!",
                             extra_tags="alert alert-success")
        word_to_guess = {'id': 0}
    else:
        position = random.randrange(count_left)
        word_to_guess = words[position]
    form = GuessForm(initial={'word_id': word_to_guess['id']})
    request.session['words'] = words
    request.session['tries'] = tries
    odsto = 100 * (count_total - count_left) / count_total

    return render(request, "words_guess_word.html", {'list': lst, 'lists': nav_lists, 
                                                     'word': word_to_guess, 'form': form, 'odsto': odsto,
                                                     'words': words, 'count_left': count_left, 
                                                     'count_total': count_total, 'tries': tries})


def show_words_list(request: HttpRequest, id: int):
    list = get_object_or_404(WordList, id=id)
    lists = WordList.objects.all().order_by('title')
    words = get_list_or_404(Word, list=list)
    return render(request, "words_list.html", {"words": words, "list": list, "lists": lists})
