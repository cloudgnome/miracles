from settings import BASE_DIR, DOMAIN

try:
    from settings import SPRITE_CATEGORIES
except:
    SPRITE_CATEGORIES = False

from shop.models import Static

version = Static.objects.first()
if not version:
    version = Static.objects.create()

version.up_version('css')
version.up_version('js')

JS_BUILD = version.js
CSS_BUILD = version.css

desktop_css = ['main','nouislider','aside','footer','header','select',

        'cart/add','cart/form',
        'catalog/products','catalog/product/buyInfo','catalog/product/gallery',
        'catalog/product/latest','catalog/product/product',
        'catalog/product/rating','catalog/product/review','catalog/product/tabs',
        'checkout/checkout','checkout/quickOrder',
        'shop/guestbook',
        'users/callBack','users/order','slider',
        'font-awesome-5.0/css/all.min','font-awesome-5.0/css/regular.min']

mobile_css = ['main','head','home','cart','categories',
                'checkout','form','guestbook','menu','order','page',
                'product','products','profile','rating','slider','select','add',
                'font-awesome-5.0/css/all.min','font-awesome-5.0/css/regular.min']

desktop_js = ['core/vanilla','core/http','core/select',
                'core/nouislider','core/validator',
                'page','cart','buy',
                'catalog/rating','catalog/gallery',
                'catalog/product','catalog/filter','catalog/products',
                'checkout/checkout','checkout/delivery','checkout/field',
                'checkout/quickOrder','checkout/callback',
                'shop/guestbook','shop/home',
                'user/profile','user/user','user/signup','user/signin',
                'user/compare','user/favorite','navigation','base']

mobile_js = ['core/vanilla','core/http','core/select',
                'core/nouislider','core/validator',
                'page','cart','buy',
                'catalog/rating','catalog/gallery',
                'catalog/product','catalog/filter','catalog/products',
                'checkout/checkout','checkout/delivery','checkout/field',
                'checkout/quickOrder','checkout/callback',
                'shop/guestbook','shop/home',
                'user/profile','user/user','user/signup','user/signin',
                'user/compare','user/favorite','navigation','base']

if SPRITE_CATEGORIES:
    desktop_css.append('categorySprite')
    mobile_css.append('categorySprite')

build_path = '{baseDir}/{DOMAIN}/static/{folder}-min{build_version}.{type}'
delete_path = '{baseDir}/{DOMAIN}/static/'
delete_pattern = '{folder}(-critical)?-min.*.{type}'
delete_sprite_pattern = 'categorySprite.*'
source_path = '{baseDir}/{DOMAIN}/static/{type}/{folder}/{name}.{type}'

try:
    from settings import DESKTOP_CSS_LIST
    desktop_css += DESKTOP_CSS_LIST
except:
    pass

try:
    from settings import MOBILE_CSS_LIST
    mobile_css += MOBILE_CSS_LIST
except:
    pass

try:
    from settings import DESKTOP_JS_LIST
    desktop_js += DESKTOP_JS_LIST
except:
    pass

try:
    from settings import MOBILE_JS_LIST
    mobile_js += MOBILE_JS_LIST
except:
    pass