from catalog.models import Category
from checkout.models import City

def serialize(items):
    result = []
    for item in items:
        result.append(item.dict())

    return result

def departaments():
    result = {'newPost':[],'delivery':[]}
    for city in City.objects.filter(type=1):
        data = city.dict()
        data['departaments'] = []
        for departament in city.departaments.all():
            data['departaments'].append(departament.dict())

        result['newPost'].append(data)

    for city in City.objects.filter(type=2):
        data = city.dict()
        data['departaments'] = []
        for departament in city.departaments.all():
            data['departaments'].append(departament.dict())

        result['delivery'].append(data)

    return result

def children(parent,category):
    childrenList = []
    for child in parent.get_children():
        category = {'id':child.id,'name':child.names(lang='ru')}
        if not child.is_leaf_node():
            category['children'] = children(child,category)
        childrenList.append(category)

    return childrenList

def categories():
    categories = []
    for parent in Category.objects.filter(active=True,parent__isnull=True):
        category = {'id':parent.id,'name':parent.names(lang='ru')}
        if not parent.is_leaf_node():
            category['children'] = children(parent,category)

        categories.append(category)

    return categories