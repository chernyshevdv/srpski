from django import forms

class GuessForm(forms.Form):
    word_id = forms.CharField(widget=forms.HiddenInput())
    guess = forms.CharField(max_length=100, label="",
                            widget=forms.TextInput(attrs={'autofocus': True, 'placeholder': 'Guess!', "autocomplete": "off"}))
