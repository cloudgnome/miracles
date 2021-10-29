from django.core.management.base import BaseCommand, CommandError
import os,re
from django.utils import timezone
from static_source_list import *
import traceback
try:
    from settings import SPRITE_CATEGORIES,STATIC_ROOT,SPRITE_SIZE
    from catalog.models import Category
except:
    SPRITE_CATEGORIES = False

parameters = { 
         'DOMAIN': DOMAIN, 
         'baseDir':BASE_DIR,
         'folder':'desktop-critical',
         'type':'css',
         'build_version':CSS_BUILD
     }

build_path = '{baseDir}/{DOMAIN}/static/{folder}-min{build_version}.{type}'

from PIL import Image

css_text = ".navigation .image.category-{id}{{background-color:{bgcolor};background-position: {x}px 10px;}}"

def sprite_icons(verbose=False):
    sprite_path = STATIC_ROOT + 'categorySprite%s.png' % CSS_BUILD

    if os.path.isfile(sprite_path):
        return

    imgs = {cat.id:{'bgcolor':cat.bgcolor,'image':cat.menu_thumb(size=SPRITE_SIZE)} for cat in Category.objects.filter(active=True,image__isnull=False)}

    images = {}
    for k,v in imgs.items():
        if imgs[k]['image']:
            images[k] = imgs[k]

    # image_width, image_height = images[next(iter(images))]['image'].size

    image_width, image_height = (SPRITE_SIZE,SPRITE_SIZE)

    if verbose:
        print("all images assumed to be %d by %d." % (image_width, image_height))

    images_count = len(images.keys())
    total_width = image_width * images_count + (images_count * 20)
    total_height = SPRITE_SIZE

    if verbose:
        print("total size %sx%s" % (total_width,total_height))
        print("creating sprite...")

    result_image = Image.new(
        mode='RGBA',
        size=(total_width,total_height),
        color=(0,0,0,0), #transparent
    )

    result_text = ''
    size = SPRITE_SIZE + 20
    location = -size
    for id,item in images.items():
        if not item['image']:
            continue
        location += size
        difference = int((size - item['image'].size[0]) / 2)

        x = (location - difference) * -1
        result_text += css_text.format(id=id,x=x,bgcolor=item['bgcolor'] or '#fff')
        result_image.paste(item['image'],(location,int((total_height - item['image'].size[1])/2)))

    result_image.save(sprite_path,format="PNG")

    if verbose:
        print(result_text)
        print("created.")

    for device in ['desktop','mobile']:
        with open(STATIC_ROOT + 'css/{device}/categorySprite.css'.format(device=device),'w') as f:
            f.write('.navigation .image{background-image: url(/static/categorySprite%s.png);}' % CSS_BUILD)
            f.write(result_text)

class Command(BaseCommand):
    help = 'Create Static'
    verbose = False

    parameters = {
        'DOMAIN':'core',
        'baseDir':BASE_DIR,
        'critical_regex':'\/\*critical\*\/(?s).*\/\*endcritical\*\/',
        'css_regex':r'(?:\n|^)(?!\@media)(?! {4}|\t)(?!@font-face).*\{',#r"(?<! )(?:(?<!@media)[a-zA-Z\- #\.,_\*0-9:>+\[\]=\'\"\(\)]){2,}\{"
        'media_regex':r'@media.*{',
        'media_text_regex':r'[\s\S]*?\}(?=\n\})\n\}',
        'fonts_regex':r'(?:\@font-face).*\{.*\}'
    }

    def add_arguments(self, parser):
        parser.add_argument('--type', nargs='+', type=str)
        parser.add_argument('-V', help="Verbose mode", nargs='+', type=bool)
        parser.add_argument('--device', help="Device Type", nargs='+', type=str)

    def handle(self, *args, **options):
        time = timezone.now()

        if options['V']:
            self.verbose = True

        if options['type']:
            self.cache(options['type'][0],options['device'][0])
        else:
            for device in ['desktop','mobile']:
                for type in ['js','css']:
                    if type == 'css' and SPRITE_CATEGORIES:
                        self.clean(delete_sprite_pattern)
                        sprite_icons(self.verbose)

                    self.cache(type,device)

        print('Time: %s' % (timezone.now() - time))
        print('Complete.')

    def clean(self,path):
        for f in [f for f in os.listdir(self.delete_path) if re.search(path,f)]:
            print('Removed: {}'.format(self.delete_path + f))
            if os.path.isfile(self.delete_path + f):
                os.remove(self.delete_path + f)

    def cache(self,type,folder):
        self.parameters.update({
            'type':type,
            'build_version':eval(type.upper() + '_BUILD'),
            'folder':folder,
        })

        self.clean(self.delete_pattern)

        with open(self.build_path,'w',encoding='utf-8') as build:
            if type == 'css':
                critical = open(self.critical_path,'a',encoding='utf-8')
                critical.seek(0)
                critical.truncate()

                self.write_fonts(build)
            else:
                critical = False

            for name in self.source_list:
                self.parameters['name'] = name
                text = self.read(critical)

                build.write(self.clear(text))

            if type == 'css':
                critical.close()
                print(self.critical_path)

            print('\nResult:')
            print(self.build_path)
            print('\n\n')

    def read(self,critical):
        try:
            file = source_path.format(**self.parameters)
            if self.verbose:
                print(file)

            with open(file,'r') as file:
                text = file.read()
        except:
            text = ''

        text = self.write_domain_source(text,critical)

        return text

    def write_domain_source(self,text,critical=None):
        self.parameters['DOMAIN'] = DOMAIN
        path = source_path.format(**self.parameters)

        self.parameters['DOMAIN'] = 'core'

        try:
            with open(path,'r',encoding='utf-8') as file:
                domain_source = file.read()
        except Exception as e:
            domain_source = ''
            if self.verbose:
                traceback.print_exc()

        if critical:
            text = self.write(critical,domain_source,text)
        else:
            text += domain_source

        if self.verbose:
            print(path)

        return text

    def write(self,file,domain_source,text):
        critical_text = self.get_critical(text)
        domain_critical_text = self.get_critical(domain_source)

        critical_text = self.analyze(critical_text,domain_critical_text)

        domain_source = self.clear_critical(domain_source)
        text = self.clear_critical(text)
        text = self.analyze(text,domain_source)
        text = self.write_media(text,domain_source)

        if critical_text:
            file.write(re.sub(r'\/\*critical\*\/|\/\*endcritical\*\/','',self.clear(critical_text)))

        return text

    def write_fonts(self,build):
        self.parameters['DOMAIN'] = DOMAIN
        self.parameters['name'] = 'main'

        try:
            with open(self.source_path,'r',encoding='utf-8') as f:
                text = ''
                for i in re.findall(self.parameters['fonts_regex'],f.read()):
                    text += i
                build.write(self.clear(text))
        except:
            pass

        self.parameters['DOMAIN'] = 'core'

    def write_media(self,text,domain_source):
        text_media = re.findall(self.parameters['media_regex'],text)
        domain_media = re.findall(self.parameters['media_regex'],domain_source)

        for i in text_media:
            if not i in domain_media:
                try:
                    source = re.search(re.escape(i) + self.parameters['media_text_regex'],text).group()
                except:
                    source = ''
                text += source

        for i in domain_media:
            media_source = re.search(re.escape(i) + self.parameters['media_text_regex'],domain_source).group()
            if not i in text_media:
                text += media_source
            else:
                media_source = media_source.replace(i,'')
                text_media_source = re.search(re.escape(i) + self.parameters['media_text_regex'],text).group()[:-1]
                for f in re.findall(r'(?: {4}|\t).*\{',media_source):
                    source = re.search(re.escape(f) + '\s*([^}]*?)\s*}',media_source).group()
                    if f in text_media_source:
                        text_media_source = re.sub(re.escape(f) + '\s*([^}]*?)\s*}',source,text_media_source)
                    else:
                        text_media_source += source

                text_media_source += '}'
                text += text_media_source

        return text

    def analyze(self,text,domain_text):
        if domain_text:
            for i in re.findall(self.parameters['css_regex'],domain_text):
                source = re.search(re.escape(i) + '\s*([^}]*?)\s*}',domain_text).group()
                if i in text:
                    try:
                        text = re.sub(re.escape(i) + '\s*([^}]*?)\s*}',source,text)
                    except:
                        print(re.escape(i) + '\s*([^}]*?)\s*}')
                else:
                    text += source

        return text

    def clear(self,text):
        return re.sub(r'[\n\t]| {4}','',text)

    def clear_critical(self,text):
        return re.sub(self.parameters['critical_regex'],'',text)

    def get_critical(self,text):
        text = re.search(self.parameters['critical_regex'],text)

        if text:
            text = text.group()

        return text

    @property
    def critical_path(self):
        self.parameters['DOMAIN'] = DOMAIN
        self.parameters['folder'] += '-critical'
        path = build_path.format(**self.parameters)

        # if self.verbose:
        #     print(path)

        self.parameters['folder'] = self.parameters['folder'].replace('-critical','')
        self.parameters['DOMAIN'] = 'core'

        return path

    @property
    def source_list(self):
        return eval("%s_%s" % (self.parameters['folder'],self.parameters['type']))

    @property
    def source_path(self):
        return source_path.format(**self.parameters)

    @property
    def build_path(self):
        self.parameters['DOMAIN'] = DOMAIN
        path = build_path.format(**self.parameters)
        self.parameters['DOMAIN'] = 'core'

        # if self.verbose:
        #     print(path)

        return path

    @property
    def delete_path(self):
        self.parameters['DOMAIN'] = DOMAIN
        path = delete_path.format(**self.parameters)
        self.parameters['DOMAIN'] = 'core'

        return path

    @property
    def delete_pattern(self):
        self.parameters['DOMAIN'] = DOMAIN
        path = delete_pattern.format(**self.parameters)
        self.parameters['DOMAIN'] = 'core'

        return path