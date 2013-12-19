from django.db import models
from datetime import date
from django.core.urlresolvers import reverse

MAX_LENGTH = 25

# Create your models here.


class Deck(models.Model):
    title = models.CharField(max_length=MAX_LENGTH)
    total_cards = models.IntegerField()

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('flashcards:deck', kwargs={'deck_id': self.id})

class Card(models.Model):
    due = models.DateField()
    front = models.CharField(max_length=MAX_LENGTH)
    back = models.CharField(max_length=MAX_LENGTH)
    deck = models.ForeignKey('Deck')
    added = models.DateField()
    right = models.IntegerField()
    wrong = models.IntegerField()
    times_answered = models.IntegerField()

    def overdue(self):
        return self.due < date.today()

    def __unicode__(self):
        return self.front

class Response(models.Model):
    date = models.DateField()
    correct = models.BooleanField()
    card = models.ForeignKey('Card')

    def __unicode__(self):
        return self.date
    
    class Meta:
        ordering = ['-date']


    

"""
  def save(self, *args, **kwargs):
        super(Model, self).save(*args, **kwargs)
"""
