import csv
from datetime import date,timedelta,datetime
from random import randint
from django.http import HttpResponse
from pymongo import MongoClient

DECKS=10
CARDS=5
RESPONSES=3

TODAY = datetime.utcnow()


def delete(collections):
    for collection in collections:
        collection.drop()

"""
generates models with sample data to test with.
"""
def generate(db):
    today = datetime.utcnow()
    decks = db.decks
    cards = db.cards
    responses = db.responses
    for i in range(0,DECKS):
        deck = {"title":'Deck' + str(i+1), "total_cards":CARDS,"user":"russ"}
        deck_id = decks.insert(deck)
        for j in range(0,CARDS):
            right = 0
            wrong = 0
            card =  {"due":today+timedelta(1-randint(1,5)),"added":today-timedelta(5+randint(1,5)),"front":'front'+str(j+1),"back":'back'+str(j+1),"deck":deck_id,"times_answered":RESPONSES,"user":deck["user"]}
            card_id = cards.insert(card)
            for k in range(0,RESPONSES):
                correct = (randint(0,1)==1)
                response = {"date":today-timedelta(days=k*2),"correct":correct,"card":card_id,"user":deck["user"],"number":k+1}
                responses.insert(response)
                if correct:
                    right += 1
                else:
                    wrong += 1
            cards.update({"deck":deck_id},{ '$set': { "right": right }, '$set':{"wrong":wrong}})

#deck_id
#user - username
#cards - card collection
def card_import(f,deck_id,db,user):
    cards_added = 0
    reader = csv.reader(f)
    if not deck_id:
        return 0
    for row in reader:
        card =  {"due":TODAY,"added":TODAY,"front":row[0],"back":row[1],"deck":deck_id,"times_answered":0,"user":user}
        card_id = db.cards.insert(card)
        cards_added += 1
    return cards_added

"""
Export cards in deck using deck.title as name
params
deck: deck model object
returns: httpresponse
"""
def export_deck(deck,cards):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = \
        'attachment; filename="{0}.csv"'.format(deck['title'] + date.today().isoformat())
    writer = csv.writer(response)
    for card in cards:
        writer.writerow([card['front'],card['back']])
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

