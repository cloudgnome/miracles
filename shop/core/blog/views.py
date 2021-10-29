# -*- coding: utf-8 -*-
from django.shortcuts import render
from blog.models import Article
from django.views.generic import View
from django.shortcuts import get_object_or_404

class ArticleView(View):
    def get(self,request,article,*args,**kwargs):
        context = {}
        context['articles'] = Article.objects.filter(active=True).order_by('-id')
        context['article'] = article
        context['url'] = article.slug

        return render(request,'blog/%s/article.html' % request.folder, context)

class ArticlesView(View):
    def get(self,request,*args,**kwargs):
        context = {}
        context['articles_list'] = Article.objects.filter(active=True).order_by('-id')
        return render(request,'blog/%s/article.html' % request.folder,context)