from django.db import models

class WordList(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self) -> str:
        return f"{self.title}"


class Word(models.Model):
    list = models.ForeignKey(to=WordList, on_delete=models.CASCADE)
    srpski = models.CharField(max_length=250)
    drugi = models.CharField(max_length=250)

    def __str__(self) -> str:
        return f"Word: {self.srpski}"
