from main.list.model import ModelAdmin
from user.models import User
from main.forms import UserForm
from django.db.models import Q

class UserAdmin(ModelAdmin):
    model = User
    form = UserForm
    head = (('id','id'),('Имя','name'),('Фамилия','lname'),('Отчество','sname'),('Email','email'),('Телефон','phone'),('su','is_admin'))
    head_search = (('по id','id'),('по имени','name__icontains'),('по фамилии','lname__icontains'),('по отчеству','sname__icontains'),('по email','email__icontains'),('по телефону','phone__contains'),())
    list_display = ('id','name','lname','sname','email','phone','admin')
    editTemplate = 'main/edit.html'

    def get_filters(self,value):
        return Q(phone__contains=value) | Q(name__icontains=value) | Q(email__icontains=value)