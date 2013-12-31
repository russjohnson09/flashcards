from django.shortcuts import render,get_object_or_404,redirect,render_to_response
from django.http import HttpResponse,Http404
from flashcards.forms import UploadFileForm,UploadForm
from datetime import date
from flashcards import utils
from django.views.decorators.csrf import ensure_csrf_cookie,csrf_exempt
import json

from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient('mongodb://rdj:rdj@ds061298.mongolab.com:61298/mydb') #practice db
db = client['mydb']
collections = [db.decks,db.cards,db.responses]

#index
def index(request):
    decks = db.decks.find()
    return render(request,'flashcards/index.html',{'decks':decks})

#model views
def deckview(request,deck_id):
    deck_id = ObjectId(deck_id)
    deck = db.decks.find_one({"_id":deck_id})
    cards = db.cards.find({"deck":deck_id})
    return render(request,'flashcards/deck.html',{'deck':deck,'cards':cards})

def cardview(request, card_id):
    card_id = ObjectId(card_id)
    card = db.cards.find_one({"_id":card_id})
    deck = db.decks.find_one({"_id":card["deck"]})
    responses = db.responses.find({"card":card_id})
    return render(request,'flashcards/card.html',{'deck':deck,'card':card, 'responses':responses})

#editing models
def deck_export(request,deck_id):
    deck_id = ObjectId(deck_id)
    deck = db.decks.find_one({"_id":deck_id})
    if deck is None:
        raise Http404
    cards = db.cards.find({"deck":deck_id})
    if cards.count() == 0:
        return HttpResponse("No cards in deck")
    return utils.export_deck(deck,cards)

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

def deck_import(request,deck_id=None):
    if not deck_id:
        raise Http404
    deck_id = ObjectId(deck_id)
    deck = db.decks.find({"_id":deck_id}) #collection of one
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            cards_added = utils.card_import(request.FILES['f'],deck_id,db,"russ")
            db.decks.update({"_id":deck_id},{"$inc":{"total_cards":cards_added}})
            return redirect('flashcards:deckview',deck_id=str(deck_id))
    else:
        form = UploadForm()
    return render(request,'flashcards/deck_import.html',{'form':form})

def deck_edit(request,deck_id):
    return render(request,'flashcards/deck_edit.html',{'deck':deck,'cards':cards})

def deck_transfer(request,deck_id):
    return HttpResponse("1")
    return render(request,'flashcards/deck_edit.html',{'deck':deck,'cards':cards})

@ensure_csrf_cookie
def deck_review(request,deck_id):
    deck_id = ObjectId(deck_id)
    deck = db.decks.find_one({"_id":deck_id})
    cards = db.cards.find({"deck":deck_id})
    return render(request,'flashcards/deck_review.html',{'deck':deck,'cards':cards})

@ensure_csrf_cookie
def submit_response(request):
    if request.is_ajax() and request.method == 'POST':
        card_id = ObjectId(request.POST['id'])
        response = int(request.POST['response'])
        utils.save_response(db,card_id,response)
        return HttpResponse(json.dumps({"success":"Saved response"}),content_type='application/json')
    return HttpResponse(json.dumps({"error":error}),content_type='application/json')

@ensure_csrf_cookie
def review(request):
    cards = Card.objects.exclude(due__gt=date.today())
    return render(request,'flashcards/review.html',{'cards':cards})


#utils
def utils_index(request):
    return render(request, 'flashcards/utils.html')

def utils_generate(request):
    utils.generate(db)
    return redirect('flashcards:utils_index')

def utils_validate(request):
    errors = utils.validate()
    return render(request, 'flashcards/error.html', {'errors':errors})

def utils_delete(request):
    utils.delete(collections)
    return redirect('flashcards:utils_index')

def errorview(request):
    errors = Error.objects.all()
    return render(request, 'flashcards/error.html',{'errors':errors})
