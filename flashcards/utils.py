import csv

from flashcards.models import Card,Deck,Response,Error
from datetime import date,timedelta,datetime
from random import randint
from django.http import HttpResponse

DECKS=10
CARDS=5
RESPONSES=3


"""
generates models with sample data to test with.
"""
def generate():
    today = date.today()
    for i in range(0,DECKS):
        d = Deck(title='Deck '+ str(i+1),total_cards=CARDS)
        d.save()
        for j in range(0,CARDS):
            right = 0
            wrong = 0
            c = Card(due=today+timedelta(1-randint(1,5)),added=today-timedelta(5+randint(1,5)),front='front'+str(j+1),back='back'+str(j+1),deck=d,right=0,wrong=0,times_answered=RESPONSES)
            c.save()
            for k in range(0,RESPONSES):
                correct = (randint(0,1)==1)
                r = Response(date=today-timedelta(days=k*2),correct=correct,card=c)
                r.save()
                if correct:
                    right += 1
                else:
                    wrong += 1
            c.right = right
            c.wrong = wrong
            c.save()

def csv_to_deck(f,deck=None):
    total = deck.total_cards
    reader = csv.reader(f)
    today = date.today()
    if not deck:
        deck = Deck(title='default',total_cards=0)
        deck.save()
    for line_num, row in enumerate(reader):
        if line_num == 0:
            deck.title = row[0]
            continue
        c = Card(due=today,added=today,front=row[0],back=row[1],deck=deck,right=0,wrong=0,times_answered=0)
        c.save()
        total += 1
    deck.total_cards = total
    deck.save()
    return deck

"""
Export deck
params
deck: deck model object
returns: httpresponse
"""
def export_deck(deck):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = \
        'attachment; filename="{0}.csv"'.format(deck.title + date.today().isoformat())
    writer = csv.writer(response)
    cards = Card.objects.filter(deck=deck)
    for card in cards:
        writer.writerow([card.front,card.back])
    return response

def validate():
    instant = datetime.now()
    true_total = 0
    decks = Deck.objects.all()
    errors = []
    errors = test_errors(10)
    for deck in decks:
        #true_total = len(Card.objects.filter(deck=deck))
        if not deck.total_cards == true_total:
            #error = Error(error_type="Validation error",text=deck.title + "[" + deck.id +"]" + "-" + deck.total_cards ":" + true_total,instant=instant,stack="NA")
            error = Error(error_type="1",text="1",instant=instant,stack="NA")
            error.save()
            errors.append(error)
    return errors


def test_errors(num):
    errors = []
    instant = datetime.now()
    for i in range(num):
        error = Error(error_type="1",text="1",instant=instant,stack="NA")
        error.save()
        errors.append(error)
    return errors

