columns = []

data = []
related = {}

from datetime import datetime
from json import dumps

def export_json(items):
    result = []
    columns = []
    dcolumns = []

    fields = items[0]._meta.fields

    for field in fields:
        columns.append(field.column)

    for i in items:
        if i.description_new.first():
            fields = i.description_new.first()._meta.fields
            break

    for field in fields:
        dcolumns.append(field.column)

    for b in items:
        item = {}
        for f in columns:
            if f == 'image':
                try:
                    item[f] = getattr(b,f).url
                except ValueError:
                    pass
            elif type(getattr(b,f)) == datetime:
                continue
            else:
                item[f] = getattr(b,f)

            item['description'] = []
            for d in b.description_new.all():
                di = {}
                for l in dcolumns:
                    if type(getattr(d,l)) == datetime:
                        continue
                    di[l] = getattr(d,l)
                item['description'].append(di)

        result.append(item)

    return dumps(result)

def mm(f,item,exclude = []):
    many_to_many_columns = {}

    for field in item._meta.many_to_many:
        model = field.related_model
        if model != item.__class__:
            # print(field.column)
            if field.column in exclude:
                continue
            many_to_many_columns[field.column] = {'Model':str(model._meta.model),'columns':[]}
            for mfield in model._meta.fields:
                many_to_many_columns[field.column]['columns'].append(mfield.column)

    f['mm'] = {}
    for key in many_to_many_columns.keys():
        f['mm'][key] = {}
        f['mm'][key]['items'] = []
        f['mm'][key]['Model'] = many_to_many_columns[key]['Model']

        for mi in getattr(item,key).all():
            mmi = {}
            for field in many_to_many_columns[key]['columns']:
                if field in exclude:
                    continue
                if '_id' in field:
                    related_item_name = field.replace('_id','')
                    if not related_item_name in related:
                        try:
                            related_item = getattr(mi,related_item_name)
                        except:
                            continue
                        related[related_item_name] = {'Model':str(related_item._meta.model),'fields':{}}
                        for rfield in related_item._meta.fields:
                            if rfield.column in exclude:
                                continue
                            if rfield.column == 'image':
                                related[related_item_name]['fields'][rfield.column] = getattr(related_item,rfield.column).name
                            else:
                                related[related_item_name]['fields'][rfield.column] = getattr(related_item,rfield.column)
                                if type(related[related_item_name]['fields'][rfield.column]) == datetime:
                                    related[related_item_name]['fields'][rfield.column] = related[related_item_name]['fields'][rfield.column].timestamp()
                        if related_item._meta.many_to_many:
                            mm(related[related_item_name],related_item,exclude)
                if field == 'image':
                    mmi[field] = getattr(mi,field).name
                else:
                    mmi[field] = getattr(mi,field)
                    if type(mmi[field]) == datetime:
                        mmi[field] = mmi[field].timestamp()

            f['mm'][key]['items'].append(mmi)

def related_items(f,item,exclude=[]):
    f['related'] = []
    for obj in item._meta.related_objects:
        model = obj.related_model
        if obj.get_accessor_name() and hasattr(item,obj.get_accessor_name()):
            name = getattr(item,obj.get_accessor_name())
            if not hasattr(name,'all'):
                continue
            objs = name.all()
            if objs:
                related = {'Model':str(model)}

                related['fields'] = []
                for field in objs[0]._meta.fields:
                    related['fields'].append(field.column)

                related['items'] = []
                for i in objs:
                    ffs = {}
                    for field in related['fields']:
                        if field == 'image':
                            ffs[field] = getattr(i,field).name
                        elif type(getattr(i,field)) == datetime:
                            ffs[field] = getattr(i,field).timestamp()
                        else:
                            ffs[field] = getattr(i,field)
                    related['items'].append(ffs)

                f['related'].append(related)
        else:
            continue

def dump(items,exclude = []):
    if not items:
        return None,None

    fields = items[0]._meta.fields

    for field in fields:
        columns.append(field.column)

    for item in items:
        f = {'Model':str(item._meta.model)}
        f['fields'] = {}

        for field in columns:
            if '_id' in field:
                related_item_name = field.replace('_id','')
                if not related_item_name in related:
                    related_item = getattr(item,related_item_name)
                    related[related_item_name] = {'Model':str(related_item._meta.model),'fields':{}}
                    for rfield in related_item._meta.fields:
                        if rfield.column == 'image':
                            related[related_item_name]['fields'][rfield.column] = getattr(related_item,rfield.column).name
                        else:
                            related[related_item_name]['fields'][rfield.column] = getattr(related_item,rfield.column)
                            if type(related[related_item_name]['fields'][rfield.column]) == datetime:
                                related[related_item_name]['fields'][rfield.column] = related[related_item_name]['fields'][rfield.column].timestamp()
                    if related_item._meta.many_to_many:
                        mm(related[related_item_name],related_item,exclude)

            value = getattr(item,field)
            f['fields'][field] = value
            if type(f['fields'][field]) == datetime:
                f['fields'][field] = f['fields'][field].timestamp()

        if item._meta.related_objects:
            related_items(f,item,exclude)

        if item._meta.many_to_many:
            mm(f,item,exclude)

        data.append(f)

    return related,data