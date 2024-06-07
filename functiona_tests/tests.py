import unittest
from django.test import LiveServerTestCase
from icecream import ic
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from words import models as words_models

MAX_WAIT = 5

class WordsTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        # Create a list to test
        self.list = words_models.WordList.objects.create(title='A test word list')
        self.words = {'word 1': 'meaning 1', 'word 2': 'meaning 2', 'word 3': 'meaning 3'}
        
        for w in self.words:
            words_models.Word.objects.create(list=self.list, srpski=w, drugi=self.words[w])


    def tearDown(self) -> None:
        self.browser.quit()
        words_models.WordList.objects.first().delete()

    def test_get_guess_form(self):
        # I open the word guessing page for a chosen List
        url = f"{self.live_server_url}/words/lists/{self.list.id}"
        ic(f"Trying URL: [{url}]")
        self.browser.get(url)
        # I see a word to guess
        word_to_guess = self.browser.find_element(By.ID, "id_guess_word").text
        self.assertIn(word_to_guess, self.words)
        # I see a form proposing me to guess the word
        # The word to guess is one in the list
