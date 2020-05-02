from .models import Article
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import Http404
from django import template

# Create your views here.

def archive(request):
    return render(request, 'templates/archive.html', {"posts":Article.objects.all()})

def get_article(request, article_id):
    try:
        post = Article.objects.get(id=article_id)
        return render(request, 'article.html', {"post": post})
    except Article.DoesNotExist:
        raise Http404

def create_post(request):
    if not request.user.is_anonymous:
        if request.method == "POST":
            # обработать данные формы, если метод POST
            form = {'text': request.POST["text"], 'title': request.POST["title"]}
            # в словаре form будет храниться информация, введенная пользователем
            if form["text"] and form["title"] and uniq(form["title"]):
                # если поля заполнены без ошибок
                Article.objects.create(text=form["text"], title=form["title"], author=request.user)
                # return redirect('get_article', article_id=article.id)
                return redirect('archive')
                # перейти на страницу поста
            else:
                # если введенные данные некорректны
                form['errors'] = u"Ошибка: оба поля должны быть заполнены, а название статьи уникальным!"
                return render(request, 'create_post.html', {'form': form})
        else:
            # просто вернуть страницу с формой, если метод GET
            return render(request, 'create_post.html', {})
    else:
        raise Http404

def uniq(title):
    posts = Article.objects.all()
    for post in posts:
        if title == post.title:
            return False
        else:
            return True