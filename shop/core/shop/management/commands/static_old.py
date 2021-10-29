from django.core.management.base import BaseCommand, CommandError
import os
from django.utils import timezone
from settings import BASE_DIR,DOMAIN
import sys, traceback
from glob import glob

class Command(BaseCommand):
    help = 'Create Static'
    commit = 41

    def remove_cache(self,pattern):
        cached = glob(pattern)
        print(cached)

        for f in glob(pattern):
            os.remove(f)

        return self.commit

    def cache(self,type,device):
        base_dir = '%s/%s/static/%s/%s' % (BASE_DIR,DOMAIN,type,device)
        base_dir_critical = '%s/%s/static/css/%s/critical' % (BASE_DIR,DOMAIN,device)
        pattern = '{base_dir}/{DOMAIN}/static/{device}-*min*.{type}'.format(**{'base_dir':BASE_DIR,'DOMAIN':DOMAIN,'type':type,'device':device})

        commit = self.remove_cache(pattern)

        critical_path = '{base_dir}/{DOMAIN}/static/{device}-critical.min{commit}.{type}'.format(**{'base_dir':BASE_DIR,'DOMAIN':DOMAIN,'type':type,'device':device,'commit':commit})
        path = '{base_dir}/{DOMAIN}/static/{device}-min{commit}.{type}'.format(**{'base_dir':BASE_DIR,'DOMAIN':DOMAIN,'type':type,'device':device,'commit':commit})

        if type == 'css':
            with open(critical_path,'w') as f:
                for root, dirs, files in os.walk(base_dir_critical):
                    for file in sorted(files):
                        try:
                            current = root+file
                            c = open(current,'r')
                            print(current)
                        except:
                            current = root+'/'+file
                            c = open(current,'r')
                            print(current)
                        text = c.read().replace('\n','').replace('\t','')
                        f.write(text)
                print('\nResult:')
                print(critical_path + '\n')

        with open(path,'w') as f:
            for root, dirs, files in os.walk(base_dir):
                for file in sorted(files):
                    if not 'critical' in root and not 'critical' in file and not '.DS_Store' in file and file != '{device}-min{commit}.{type}'.format(**{'device':device,'type':type,'commit':commit}):
                        try:
                            current = root+file
                            c = open(current,'r')
                            print(current)
                        except:
                            current = root+'/'+file
                            c = open(current,'r')
                            print(current)
                        text = c.read().replace('\n','').replace('\t','')
                        f.write(text)
            print('\nResult:')
            print(path + '\n')

    def add_arguments(self, parser):
        parser.add_argument('--type', nargs='+', type=str)
        parser.add_argument('--device', nargs='+', type=str)

    def handle(self, *args, **options):
        time = timezone.now()
        type = options['type'][0] if options['type'] else 'css'
        device = options['device'][0] if options['device'] else 'desktop'

        try:
            self.cache(type=type,device=device)
        except Exception as e:
            traceback.print_exc(file=sys.stdout)

        print('Потрачено времени: %s' % (timezone.now() - time))
        print('Завершено.')