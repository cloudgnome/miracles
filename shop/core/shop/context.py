# -*- coding: utf-8 -*-
from shop.models import Language,Settings
from django.utils.translation import gettext as _
from catalog.models import Product,Category,Brand,Tag,City,Page,Slug,Popular
from blog.models import Article
from re import sub
from settings import CACHE_URL,BASE_URL,ADMIN_BASE_URL,PROTOCOL
from os.path import isfile
from shop.models import Static

try:
    from settings import YOUTUBE_LINK,FACEBOOK_LINK,PHONES,ADDRESS,GOOGLE_SITE_VERIFICATION,GOOGLE_TAG,GOOGLE_ANALYTICS
except:
    YOUTUBE_LINK = FACEBOOK_LINK = PHONES = ADDRESS = GOOGLE_SITE_VERIFICATION = GOOGLE_TAG = GOOGLE_ANALYTICS = ''

try:
    from settings import IOS_APP
except:
    IOS_APP = False

def default(request):
    version = Static.objects.first()
    CSS_BUILD = version.css
    JS_BUILD = version.js

    shop_settings = Settings.objects.values('facebook_id','attention_message','phones','emails','google_analytics','google_adwords','google_tag','google_verification').first()

    context = {}
    context['language'] = '/%s' % request.LANGUAGE_CODE if request.LANGUAGE_CODE != 'ru' else ''
    context['lang'] = request.LANGUAGE_CODE

    if not request.is_ajax():
        context['BASE_URL'] = BASE_URL
        context['PROTOCOL'] = PROTOCOL
        context['host'] = BASE_URL
        context['ADMIN_BASE_URL'] = ADMIN_BASE_URL
        context['CSS_BUILD'] = CSS_BUILD
        context['JS_BUILD'] = JS_BUILD
        context['GOOGLE_SITE_VERIFICATION'] = shop_settings.get('google_verification') or ''
        context['GOOGLE_TAG'] = shop_settings.get('google_tag') or ''
        context['GOOGLE_ANALYTICS'] = shop_settings.get('google_analytics') or ''
        context['GOOGLE_ADWORDS'] = shop_settings.get('google_adwords') or ''
        context['FACEBOOK_ID'] = shop_settings.get('facebook_id') or ''
        context['YOUTUBE_LINK'] = YOUTUBE_LINK
        context['FACEBOOK_LINK'] = FACEBOOK_LINK

        context['cities'] = City.objects.all()
        context['navigation'] = Category.objects.filter(parent__isnull=True)
        context['languages'] = Language.objects.all()
        try:
            context['langISOcode'] = Language.objects.get(code=context['lang']).ISOcode
        except: 
            context['langISOcode'] = 'ru'
        context['image'] = 'https://%s/static/image/igroteka/og_logo.png' % BASE_URL

        root = '{CACHE_URL}cache/html/{device}/{lang}/static/'.format(device=request.folder,lang=request.LANGUAGE_CODE,CACHE_URL=CACHE_URL)
        if not isfile(root + 'categories.html'):
            from catalog.views import StaticView
            StaticView(request,root)

        context['nav'] = root + 'categories.html'
        context['popular'] = Popular.objects.filter(product__is_available=True)
        context['latest'] = Product.objects.filter(is_available=True).order_by('-id')[:6]
        context['header_menu'] = Page.objects.filter(position=1)
        try:
            context['attention_message'] = Settings.objects.values('attention_message').first().get('attention_message')
        except:
            pass
        context['footer_menu'] = Page.objects.filter(position=2)
        context['ADDRESS'] = ADDRESS
        context['EMAIL'] = shop_settings.get('emails').split(',')[0]
        context['PHONES'] = shop_settings.get('phones').split(',')
        context['IOS_APP'] = IOS_APP

    return context

def meta(request):
    context = default(request)

    if not request.is_ajax():
        page = request.GET.get('page')
        context['url'] = sub(r'^(/ua)?/','',request.path)

        try:
            slug = Slug.objects.get(slug=context['url'])
        except Slug.DoesNotExist:
            if context['url'] == '':
                try:
                    slug = Slug.objects.get(slug__isnull=True)
                except Slug.DoesNotExist:
                    slug = None
            else:
                slug = None

        if slug:
            Obj = eval(slug.model)
            try:
                obj = Obj.objects.get(id=slug.model_id)
                try:
                    description = obj.description.get(language__code=request.LANGUAGE_CODE)
                except:
                    description = obj.description.first()


                if description:
                    context['title'] = description.title
                    context['meta_description'] = description.meta_description
                    context['meta_keywords'] = description.meta_keywords
                    context['url'] = obj.get_url

                    context['h1'] = description.name

                    if page:
                        context['title'] = "{} {} {}".format(context['title'], _(' Страница '), page)
                        context['h1'] = "{} {} {}".format(context['h1'], _(' Страница '), page)
                        context['meta_description'] = "{} {} {}".format(context['meta_description'],_(' Страница '), page)

                    context['image'] = "https://%s%s" % (request.get_host(),obj.meta_image)
                    if not page:
                        context['description'] = description.text or ''
                else:
                    context['title'] = getattr(obj,'title') or getattr(obj,'name')
                    context['meta_description'] = getattr(obj,'meta_description')
                    context['meta_keywords'] = getattr(obj,'meta_keywords')

                if request.user.is_admin:
                    context['edit_url'] = '%s/%s/%s' % (ADMIN_BASE_URL,slug.model,obj.id)

                if isinstance(obj,City):
                    context['cities'] = City.objects.exclude(id=obj.id)
            except Obj.DoesNotExist:
                pass

    return context