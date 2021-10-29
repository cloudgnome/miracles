from django.core.management.base import BaseCommand, CommandError
import os,re
from django.utils import timezone
from settings import BASE_DIR, CACHE_DIR, DOMAIN, JS_BUILD, CSS_BUILD

try:
    from settings import SPRITE_CATEGORIES
except:
    SPRITE_CATEGORIES = None

class Command(BaseCommand):
    help = 'Create Static'
    css = ['font-awesome-5.0/css/all.min','select','main','login','categories','category','edit',
            'list','order','menu','settings','nouislider','radio','checkbox','editor']

    js = ['core/core','core/select','core/sortable',
            'core/nouislider','core/history','core/form',
            'core/autocomplete',
            'views/base','views/login',
            'views/edit/autocomplete',
            'views/edit/base','views/edit/fgk','views/edit/brand','views/edit/cart',
            'views/edit/category','views/edit/default',
            'views/edit/gallery','views/edit/order',
            'views/edit/product',
            'views/list/base','views/list/category',
            'views/list/order','views/list/product','views/list/settings',
            'core/http',
            'urls','menu','templates','core/chart.min',
            'core/editor/header','core/editor/editor','core/editor/checklist',
            'core/editor/code','core/editor/delimiter','core/editor/embed',
            'core/editor/inline-code','core/editor/link','core/editor/list',
            'core/editor/marker','core/editor/quote','core/editor/img',
            'core/editor/table','core/editor/warning','core/editor/html']

    buildPath = '{baseDir}/{DOMAIN}/static/min{build}.{type}'
    base_path = '{baseDir}/core/static/{type}/{name}.{type}'
    delete_path = '{baseDir}/{DOMAIN}/static/'
    domain_path = '{baseDir}/{DOMAIN}/static/{type}/{name}.{type}'

    dirname = os.path.dirname(f'{BASE_DIR}')
    category_sprite = '{dirname}/shop/{DOMAIN}/static/css/desktop/categorySprite.css'.format(dirname=dirname,DOMAIN=DOMAIN)

    def clean(self):
        path = self.delete_path.format(baseDir=CACHE_DIR,DOMAIN=DOMAIN)

        for f in [f for f in os.listdir(path) if re.search('min.*',f)]:
            print('Removed: {}'.format(path + f))
            if os.path.isfile(path + f):
                os.remove(path + f)

    def cache(self,type,buildType):
        buildPath = self.buildPath.format(baseDir=CACHE_DIR,DOMAIN=DOMAIN,type=type,build=buildType)
        category_sprite = self.category_sprite.format(DOMAIN=DOMAIN)

        buildDir = f'{CACHE_DIR}/{DOMAIN}'
        if not os.path.isdir(buildDir):
            os.makedirs(buildDir,mode=0o777)

        with open(buildPath,'w',encoding='utf-8') as build:
            for name in getattr(self,"%s" % type):
                try:
                    file = self.domain_path.format(baseDir=BASE_DIR,type=type,name=name)
                    file = open(file)
                except:
                    file = self.base_path.format(baseDir=BASE_DIR,type=type,name=name)
                    file = open(file)

                print(file)

                text = file.read().replace('\n','').replace('\t','')
                build.write(text)

            if SPRITE_CATEGORIES and type == 'css':
                with open(category_sprite,'r') as f:
                    build.write(f.read())

            print('\nResult:')
            print(buildPath)
            print('\n\n')

    def add_arguments(self, parser):
        parser.add_argument('--type', nargs='+', type=str)

    def handle(self, *args, **options):
        time = timezone.now()

        self.clean()

        if options['type']:
            self.cache(options['type'][0],buildType=eval(options['type'][0].upper() + '_BUILD'))
        else:
            for t in ['css','js']:
                self.cache(t,buildType=eval(t.upper() + '_BUILD'))

        print('Time: %s' % (timezone.now() - time))
        print('Complete.')