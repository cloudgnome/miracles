from main.list.model import ModelAdmin
from blog.models import Article
from main.forms import ArticleForm

class ArticleAdmin(ModelAdmin):
    model = Article
    form = ArticleForm
    head = (('id','id'),('Название','name'))
    head_search = (('по id','id'),('по названию','description__name__icontains'))
    list_display = ('id','name')