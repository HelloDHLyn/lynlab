# -*- coding: utf-8 -*-

from django.db import models
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect

class Article(models.Model):
    class Meta:
        verbose_name = u'wiki'
        ordering = ['title']

    title = models.CharField(verbose_name=u'title', max_length=256)
    subtitle = models.CharField(verbose_name=u'subtitle', max_length=256, null=True, default='')
    content = models.TextField(u'content', blank=True, default='')
    created = models.DateTimeField(auto_now_add=True, verbose_name=u'date')
    last_modified = models.DateTimeField(auto_now_add=True, null=True, verbose_name=u'modified')

    def __unicode__(self):
        return self.title

class ModifyHistory(models.Model):
    class Meta:
        verbose_name = u'wiki_history'
        ordering = ['timestamp']

    title = models.CharField(verbose_name=u'title', max_length=256)
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name=u'timestamp')
    editor = models.CharField(verbose_name=u'editor', max_length=256)

def search(request):
    req_title = request.POST['title']
    try:
        Article.objects.get(title=req_title)
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('wikiarticle', kwargs={'pk': req_title}))
    else:
        return HttpResponseRedirect(reverse('wikiarticle', kwargs={'pk': req_title}))

@login_required(login_url='/accounts/login/')
def modify(request):
    if request.user.is_authenticated():
        username = request.user.username
    else:
        return HttpResponse(status=201)

    req_title = request.POST['title']
    req_content = filter_words(request.POST['content'])

    try:
        article = Article.objects.get(title=req_title)
    except ObjectDoesNotExist:
        new_article = Article(title=req_title, content=req_content)
        new_article.save()
    else:
        article.content = req_content
        article.save()

    new_history = ModifyHistory(title=req_title, editor=username)
    new_history.save()

    return HttpResponseRedirect(reverse('wikiarticle', kwargs={'pk': req_title}))

filter_keywords = ['<script>', '</script>', '<h1>', '</h1>', '<h2>', '</h2>', '<h3>', '</h3>', '<h4>', '</h4>', '<h5>', '</h5>', '<h6>', '</h6>', 
                   '<a', '</a>', '<code>', '</code>', '<iframe>', '</iframe>', '<div>', '</div>', '<input>', '<textarea>', '</textarea>', '<style>', '</style>',
		   '<br>', '<br/>', '<br />', '<img', '</img>', '<strong>', '</strong>', '<b>', '</b>', '<i>', '</i>', '<u>', '</u>']

def filter_words(content):
    for keyword in filter_keywords: 
        content = content.replace(keyword, '')

    return content