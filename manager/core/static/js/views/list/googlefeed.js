class GoogleFeedList extends List{
    constructor(){
        super();
        View.variants($('#category'),'category',function(event){view.categoryAutocomplete(event.target)});
        View.variants($('#brand'),'brand',function(event){view.brandAutocomplete(event.target)});
        $('#addProducts').on('click',this.addProducts.bind(this));
        $('#filters button').on('click',this.filter);
    }
    filter(){
        var filters = $('#filters').serializeJSON();
        for(key of view.url.searchParams.keys()){
            view.url.searchParams.delete(key);
        }
        for(var key of Object.keys(filters)){
            view.url.searchParams.set(key,filters[key]);
        }
        http.action = function(){
            $('#items').html(http.response);
        };
        view.url.searchParams.set('block','reload');
        view.url.searchParams.set('googlefeed__isnull','True');
        view.url.searchParams.set('all',true);
        http.get('/product/list' + view.url.search);
        $('#filters').hide();
    }
    addProducts(){
        http.action = function(){
            if(http.json && http.json.result)
                http.alert('Добавлено');
        };
        var items = [];
        for(var item of $('.item input:checked'))
            items.push(item.get('value'));
        http.post('/addGoogleProducts',{'items':items});
    }
    categoryAutocomplete(target){
        var category = $('#category');
        category.find('.variants')[0].hide();
        category.find('input')[0].value = target.text();
    }
    brandAutocomplete(target){
        var brand = $('#brand');
        brand.find('.variants')[0].hide();
        brand.find('input')[0].value = target.text();
    }
}