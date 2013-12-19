from django.shortcuts import render,get_object_or_404,redirect,render_to_response
#from django.http import HttpResponse
from flashcards.models import * #TODO specific imports
from flashcards.forms import *
from datetime import date
from flashcards import utils
import csv
from django.views.decorators.csrf import ensure_csrf_cookie,csrf_exempt

from django.http import *
from django.template import RequestContext
from django.utils import simplejson
import socket
import json

#http://www.fir3net.com/Django/how-do-i-use-ajax-along-side-django.html
#http://jbjose.com/index.php/2013/07/tutorial-using-django-and-jquery/
#http://hunterford.me/django-messaging-for-ajax-calls-using-jquery/

@ensure_csrf_cookie
def ajax(request):
    if request.is_ajax() and request.method == 'POST':
        title = request.POST['title']
        response = {}
        response['note'] = 'Saved Successfully'
        response['note'] = title
        return HttpResponse(json.dumps(response),content_type='application/json')
        #else:
            #return HttpResponse(json.dumps({'note':'Error'}),content_type='application/json')
    elif request.is_ajax() and request.method == 'GET':
        title = len(request.GET)
        response = {}
        response['note'] = 'Saved Successfully'
        response['note'] = title
        return HttpResponse(json.dumps(response),content_type='application/json')
    else:
        return render(request,'flashcards/ajax.html')

def test(request):
    return render(request,'')


def export(request,deck_id):
    deck = get_object_or_404(Deck,pk=deck_id)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = \
        'attachment; filename="{0}.csv"'.format(deck.title + date.today().isoformat())
    writer = csv.writer(response)
    export_deck(writer,deck)
    return response

def export_deck(writer,deck):
    cards = Card.objects.filter(deck=deck)
    for card in cards:
        writer.writerow([card.front,card.back])

@ensure_csrf_cookie
def review(request,deck_id):
    deck = get_object_or_404(Deck,pk=deck_id)
    cards = Card.objects.filter(deck=deck).exclude(due__gt=date.today())
    return render(request,'flashcards/review.html',{'deck':deck,'cards':cards})


def upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            deck = csv_to_deck(request.FILES['f'])
            return redirect(deck)
    else:
        form = UploadFileForm()
    return render(request,'flashcards/upload.html',{'form':form})

def index(request):
    #utils.populate()
    decks = Deck.objects.all()
    return render(request,'flashcards/index.html',{'decks':decks})

#def index(request):
#    return render(request,'flashcards/index.html')

def deckview(request, deck_id):
    deck = get_object_or_404(Deck,pk=deck_id)
    cards = Card.objects.filter(deck=deck)
    return render(request,'flashcards/deck.html',{'deck':deck,'cards':cards})

def cardview(request, card_id):
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
    today = date.today()
    card_list = []
    for i in cards:
        c = Card(due=today,added=today,front='front'+str(i),back='back'+str(i),deck=d)
        card_list.append(c)
    return card_list


def csv_to_deck(f):
    today = date.today()
    reader = csv.reader(f)
    deck = Deck(title='default',total_cards=0)
    deck.save()
    total = 0
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
