from django.shortcuts import render,get_object_or_404
from flashcards.models import * #TODO specific imports
from datetime import date
from flashcards import utils


def index(request):
    utils.populate()
    decks = Deck.objects.all()
    return render(request,'flashcards/index.html',{'decks':decks})

#def index(request):
#    return render(request,'flashcards/index.html')

def deck(request, deck_id):
    deck = get_object_or_404(Deck,pk=deck_id)
    cards = Card.objects.filter(deck=deck)
    return render(request,'flashcards/deck.html',{'deck':deck,'cards':cards})

def card(request, card_id):
    card = get_object_or_404(Card,pk=card_id)
    responses = Response.objects.filter(card=card)
    return render(request,'flashcards/card.html',{'deck':card.deck,'card':card, 'responses':responses})

"""
deck - number of decks
cards - cards per deck
"""
def create_flashcards(decks,cards):
    today = date.today()
    for i in range(0,decks):
        d = Deck(title='Deck '+str(i),total_cards=0)
        d.save()
        for j in range(0,cards):
            c = Card(due=today,front='front'+str(j),back='back'+str(j),deck=d)
            c.save()
        d.total_cards = cards
        d.save()

            

def create_cards(cards):
    card_list = []
    for i in cards:
        c = Card(due=today,added=today,front='front'+str(i),back='back'+str(i),deck=d)
        card_list.append(c)
    return card_list


    
    

"""
def upgrade():
    today = date.today()
    for card in Card.objects.all():
        card.added = today
    card.save()
"""

#question get_object_or_404(Question, pk=qid)


"""
from django.test import TestCase
from myapp.models import Animal

class AnimalTestCase(TestCase):
    def setUp(self):
        Animal.objects.create(name="lion", sound="roar")
        Animal.objects.create(name="cat", sound="meow")

   def test_animals_can_speak(self):
        lion = Animal.objects.get(name="lion")
        cat = Animal.objects.get(name="cat")
        self.assertEqual(lion.speak(), 'The lion says "roar"')
        self.assertEqual(cat.speak(), 'The cat says "meow"')

  def save(self, *args, **kwargs):
        super(Model, self).save(*args, **kwargs)
"""
