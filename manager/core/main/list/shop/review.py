from main.list.model import ModelAdmin
from shop.models import Review
from shop.forms import ReviewForm

class ReviewAdmin(ModelAdmin):
    model = Review
    form = ReviewForm
    head = (('id','id'),('Автор','author'),('Название','name'),('Дата','created_at'))
    head_search = (('по id','id'),('по автору','author__icontains'),('по названию','name__icontains'),())
    list_display = ('id','author','title','created_at','activity')
    editTemplate = 'main/edit.html'