from django.shortcuts import render,get_object_or_404,redirect,render_to_response
from django.http import HttpResponse,Http404
from django.views.decorators.csrf import ensure_csrf_cookie,csrf_exempt
import json

from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient('mongodb://rdj:rdj@ds061298.mongolab.com:61298/mydb') #practice db
db = client['mydb']
collections = [db.blogs,db.comments]

#index
def index(request):
    blogs = db.blogs.find()
    return render(request,'blog/index.html',{'blogs':blogs})

#model views
def blog_view(request,blog_id):
    blog_id = ObjectId(blog_id)
    blog = db.blogs.find_one({"_id":blog_id})
    comments = db.comments.find({"blog":blog_id})
    return render(request,'blog/blog.html',{'blog':blog,'comments':comments})


#utils
def create(request):
    blogs = db.blogs
    comments = db.comments
    for i in range(0,10):
        blog = {"title":'Deck' + str(i+1), "txt":"asdfk;ljasd;lfkj;slakdfj","user":"russ"}
        blog_id = blogs.insert(blog)
        for j in range(10,20):
            comment = {'user':'user'+str(j), 'txt':'This is commnet' + str(j), 'blog':blog_id}
            comments.insert(comment)
    return redirect('blog:index')

def delete(request):
    for collection in collections:
        collection.drop()
    return redirect('blog:index')

