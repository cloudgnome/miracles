var urlpatterns = {
    "^\\?(?<filters>[\\s\\S]*)$":{"GET":ReloadList,"POST":ReloadList},
    "^(?<origin>(http(s)?)://[a-zа-я0-9.-]+)?/(?<Model>[A-Z][a-z]+)/(?<id>[0-9]+)?(#(?<anchor>[a-z]+))?":{"GET":Edit},
    "^(?<origin>(http(s)?)://[a-zа-я0-9.-]+)?/(?<Model>[A-Z][a-z]+)(\\?(?<filters>[\s\S]*))?":{"GET":List,"POST":ReloadList},
    "^(?<origin>(http(s)?)://[a-zа-я0-9.-]+)?/$":{"GET":Settings},
};