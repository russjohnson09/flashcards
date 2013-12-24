from django.shortcuts import render,get_object_or_404,redirect,render_to_response
from django.http import HttpResponse
from flashcards.models import Deck,Card,Response,Error
from flashcards.forms import UploadFileForm,UploadForm
from datetime import date
#from flashcards.utils import generate,csv_to_deck,export_deck,validate,generate_mongo
from flashcards import utils
from django.views.decorators.csrf import ensure_csrf_cookie,csrf_exempt
import json
from django.http import Http404

from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient()
db = client['mydb']

#index
def index(request):
    decks = db.decks.find()
    return render(request,'flashcards/index.html',{'decks':decks})

#model views
def deckview(request,deck_id):
    deck = db.decks.find_one({"_id":ObjectId(deck_id)})
    cards = db.cards.find({"deck":ObjectId(deck_id)})
    return render(request,'flashcards/deck.html',{'deck':deck,'cards':cards})

def cardview(request, card_id):
    card = get_object_or_404(Card,pk=card_id)
    responses = Response.objects.filter(card=card)
    return render(request,'flashcards/card.html',{'deck':card.deck,'card':card, 'responses':responses})

#editing models
def deck_export(request,deck_id):
    deck = get_object_or_404(Deck,pk=deck_id)
    return utils.export_deck(deck)

@ensure_csrf_cookie
def deck_create(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            deck = utils.csv_to_deck(request.FILES['f'])
            return redirect(deck)
    else:
        form = UploadFileForm()
    return render(request,'flashcards/deck_create.html',{'form':form})

def deck_import(request,deck_id):
    deck = get_object_or_404(Deck,pk=deck_id)
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            deck = utils.csv_to_deck(request.FILES['f'],deck)
            return redirect(deck)
    else:
        form = UploadForm()
    return render(request,'flashcards/deck_import.html',{'form':form})

def deck_edit(request,deck_id):
    deck = get_object_or_404(Deck,pk=deck_id)
    cards = Card.objects.filter(deck=deck).exclude(due__gt=date.today())
    return render(request,'flashcards/deck_edit.html',{'deck':deck,'cards':cards})

def deck_transfer(request,deck_id):
    return HttpResponse("1")
    deck = get_object_or_404(Deck,pk=deck_id)
    cards = Card.objects.filter(deck=deck).exclude(due__gt=date.today())
    return render(request,'flashcards/deck_edit.html',{'deck':deck,'cards':cards})

@ensure_csrf_cookie
def deck_review(request,deck_id):
    deck = get_object_or_404(Deck,pk=deck_id)
    cards = Card.objects.filter(deck=deck) #.exclude(due__gt=date.today())
    return render(request,'flashcards/deck_review.html',{'deck':deck,'cards':cards})

@ensure_csrf_cookie
def review(request):
    cards = Card.objects.exclude(due__gt=date.today())
    return render(request,'flashcards/review.html',{'cards':cards})


#utils
def utils_index(request):
    return render(request, 'flashcards/utils.html')

def utils_generate(request):
    #generate()
    utils.generate_mongo()
    return redirect('flashcards:utils_index')

def utils_validate(request):
    errors = utils.validate()
    return render(request, 'flashcards/error.html', {'errors':errors})

def utils_delete(request):
    utils.delete()
    return redirect('flashcards:utils_index')

def errorview(request):
    errors = Error.objects.all()
    return render(request, 'flashcards/error.html',{'errors':errors})


#test views

@ensure_csrf_cookie
def ajax(request):
    if request.is_ajax() and request.method == 'POST':
        title = request.POST['title']
        response = {}
        response['note'] = "You're deck " + title + " Saved Successfully"
        deck = Deck(title=title,total_cards=0)
        deck.save()
        return HttpResponse(json.dumps(response),content_type='application/json')
    elif request.is_ajax() and request.method == 'GET':
        title = len(request.GET)
        response = {}
        response['note'] = 'Saved Successfully'
        response['note'] = title
        return HttpResponse(json.dumps(response),content_type='application/json')
    else:
        return render(request,'flashcards/ajax.html')
