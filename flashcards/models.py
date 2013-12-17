from django.db import models

MAX_LENGTH = 25

# Create your models here.


class Deck(models.Model):
    title = models.CharField(max_length=MAX_LENGTH)
    total_cards = models.IntegerField()
    def __unicode__(self):
        return self.title

class Card(models.Model):
    due = models.DateField()
    front = models.CharField(max_length=MAX_LENGTH)
    back = models.CharField(max_length=MAX_LENGTH)
    deck = models.ForeignKey('Deck')
    #added = models.DateField()

    def __unicode__(self):
        return self.front
    

"""
  def save(self, *args, **kwargs):
        super(Model, self).save(*args, **kwargs)
"""
