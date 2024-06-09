import unittest
from django.test import LiveServerTestCase
from icecream import ic
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time 
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
        url = f"{self.live_server_url}/words/lists/{self.list.id}/guess"
        self.browser.get(url)
        # I see a word to guess
        word_to_guess = self.browser.find_element(By.ID, "id_word_srpski").text
        # The word to guess is one in the list
        self.assertIn(word_to_guess, self.words)
        # I see a form proposing me to add the drugi word (to guess)
        
    
    def test_guess_correct_word(self):
        # Open the word guessing page
        url = f"{self.live_server_url}/words/lists/{self.list.id}/guess"
        self.browser.get(url)

        # Get the word to guess from element id=id_word_srpski
        word_to_guess = self.browser.find_element(By.ID, "id_word_srpski").text

        # Find the word in the list
        word = self.list.word_set.filter(srpski=word_to_guess).first()
        self.assertIsNotNone(word, f"Must find a guessed word in the DB")
        # Get the correct guess
        correct_guess = word.drugi
        # Fill it into the input box with id=id_word_drugi
        guess_form_element = self.browser.find_element(By.ID, "id_guess")
        guess_form_element.send_keys(correct_guess)
        # Send the form by clicking "Submit" button
        guess_form_element.send_keys(Keys.ENTER)
        # Get the reply confirming the guess is correct
        time.sleep(1)
        page_text = self.browser.find_element(By.TAG_NAME, "body").text
        self.assertIn("Tako je!", page_text)

    def test_guess_incorrect_word(self):
        # Open the word guessing page
        url = f"{self.live_server_url}/words/lists/{self.list.id}/guess"
        self.browser.get(url)

        # Get the word to guess from element id=id_word_srpski
        word_to_guess = self.browser.find_element(By.ID, "id_word_srpski").text

        # Find the word in the list
        incorrect_guess = "Abrakadabra!"
        # Fill it into the input box with id=id_word_drugi
        guess_form_element = self.browser.find_element(By.ID, "id_guess")
        guess_form_element.send_keys(incorrect_guess)
        # Send the form by clicking "Submit" button
        guess_form_element.send_keys(Keys.ENTER)
        # Get the reply confirming the guess is correct
        time.sleep(1)
        page_text = self.browser.find_element(By.TAG_NAME, "body").text
        self.assertNotIn("Tako je!", page_text)
        self.assertIn("Ne tačno...", page_text)
