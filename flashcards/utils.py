from flashcards.models import * #TODO specific imports
from datetime import date,timedelta
from random import randint

DECKS=10
CARDS=5
RESPONSES=3


"""
Populates models with sample data to test with.
"""
def populate():
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
    return

