class Page{
    constructor(){
        this.navigation = null;
        this.searchQuery = '';
        this.progress = false;
        this.timeout = false;
        this.user = new User();
        this.cartQty = $('.cart .items_qty');
        this.menuBlock = $('#menu');
        this.mainBlock = $('#main');
        this.searchWidget = $('#search');
        this.navContainer = $('#navigation .head')[0];
        this.scrollUpButton = $("#scroll-up");

        this.addCart = $('#add-cart');
        this.addCartText = $('#add-cart span.name')[0];
        this.favoriteButton = $('header .profile.favorite');
        this.compareButton = $('header .profile.compare');

        $('.call-back').on('click', this.callback.bind(this));

        $('.categories-button').on('click',this.openCategories.bind(this));

        try{
            JSON.parse(storage.cart);
        }catch(e){
            this.clearCart();
        }

        if(!storage.qty || storage.qty == 'NaN')
            storage.qty = Object.keys(cart).length;

        this.cartQty.text(storage.qty);

        if(storage.qty && storage.qty != 0)
            $('#panel .cart').show();

        this.cart = JSON.parse(storage.cart);

        $('#searchButton').on('click',this.searchButton.bind(this));

        $("#scroll-up").on('click',function(){
            scrollTop();
        });

        $('main .noselect').on('contextmenu',function(){
            return false;
        });

        $('#phonesButton').on('click',this.phones);

        $('#search input[type=text]').on('input paste keypress',this.search.bind(this));
        $('#search #query').on('focus click',this.searchfocus.bind(this));
        $('.autocomplete').on('scroll click',function(event){event.stopPropagation();});

        $('#bg').on('click',this.hideBg.bind(this));

        $('.cart').on('click',this.openCart.bind(this));

        var href = new URL(location.href);
        if(href.searchParams)
            var q = href.searchParams.get('q');
        else{
            var query = getQueryParams(location.search);
            var q = query.q;
        }

        $('body').on('click',(e) => {
            if($('.autocomplete').css('display') == 'block'){
                $('.autocomplete').hide();
            }
            this.menuBlock.removeClass('active');
            this.mainBlock.removeClass('active');
        });

        this.menuBlock.on('click',(e) =>{
            e.stopPropagation();
            return false;
        });

        addEventListener('scroll',this.scroll.bind(this));

        if(!storage.compare)
            storage.compare = '[]';
        this.compare = JSON.parse(storage.compare);
        try{
            $('header .fa-balance-scale')[0].prev().text(this.compare.length);
        }catch(e){

        }

        if(!storage.favorite)
            storage.favorite = '[]';
        this.favorite = JSON.parse(storage.favorite);
        try{
            $('header .fa-star')[0].prev().text(this.favorite.length);
        }catch(e){
            
        }

        if(this.favorite && this.favorite.length){
            this.favoriteButton.show();
        }
        if(this.compare && this.compare.length){
            this.compareButton.show();
        }
    }
    scroll(e){
        if(window.scrollY > 150){
            this.scrollUpButton.show();
        }else{
            this.scrollUpButton.hide();
        }
    }
    callback(){
        var that = this;
        http.action = function(){
            that.renderForm();
            that.callback = new Callback();
        };
        http.get(`${language}/checkout/callback/`);
    }
    openCategories(e){
        var main_container = $('main .navigation')[0];
        var container = $('#menu .navigation')[0];

        if(!this.navigation){
            if(main_container){
                container.html(main_container.html());
                this.navigation = new Navigation(container);
            }
            else{
                var that = this;
                http.action = function(){
                    container.html(http.response);
                    that.navigation = new Navigation(container);
                };
                http.get(language + '/categories');
            }
        }

        this.menuBlock.active();
        this.mainBlock.active();

        $('#navigation .back').removeClass('active');

        e.stopPropagation();
        return false;
    }
    searchButton(){
        this.searchWidget.active();
    }
    phones(){
        $('header .phones').active();
    }
    clearCart(){
        storage.cart = "{}";
        storage.qty = 0;
        this.cartQty.text('0');
        this.cart = {};
    }
    hideBg(event){
        var target = event.target;
        target.hide();
        $('#form').removeClass('show');
    }
    hideMessage(){
        if(this.addCart.hasClass('active'))
            this.addCart.active();
        if(this.messageTimeout)
            clearTimeout(this.messageTimeout)
    }
    message(text){
        if(this.addCart && this.addCartText){
            this.addCartText.text(text);
            if(!this.addCart.hasClass('active')){
                this.addCart.active();

                var that = this;
                if(this.messageTimeout)
                    clearTimeout(this.messageTimeout);
                this.messageTimeout = setTimeout(function(){
                    that.addCart.active();
                },7000);
            }
        }
    }
    renderForm(){
        $('#form').html(http.response);
        $('#form').addClass('show');
        $('#form .close').addClass('show');
        $('#bg').show();
        $('#form .close').on('click',function(){
            $('#form').removeClass('show');
            $('#bg').hide();
            this.removeClass('show');
        });
    }
    openCart(){
        var that = this;
        http.action = function(){
            that.renderForm();
            that.cartObject = new Cart();
            that.hideMessage();
        };
        var data = JSON.parse(storage.cart);
        data['csrfmiddlewaretoken'] = csrf_token;
        http.post(language +'/cart/',data);
    }
    autocomplete(query){
        if(query != this.searchQuery){
            this.searchQuery = query;
            http.action = function(){
                $('.autocomplete').html(http.responseText);
                $('.autocomplete').show();
            };
            http.get(`${language}/search?q=${this.searchQuery}&autocomplete=1`);
        }
        return false;
    }

    searchfocus(event){
        var that = this;
        if(this.searchQuery && this.searchQuery.length > 2){
            if($('#search .autocomplete').length && $('#search .autocomplete')[0].children.length == 0){
                http.action = function(){
                    $('#search .autocomplete').html(http.responseText);
                };
                http.get(`/search?q=${this.searchQuery}&autocomplete=1`);
            }
            $('#search .autocomplete').show();
        }
        event.stopPropagation();
        return false;
    }
    search(event){
        var that = this;
        if(this.timeout)
            clearTimeout(this.timeout);
        this.timeout = setTimeout(function(){
            var query = $('#search input[type=text]')[0].value;
            if(query.length > 2){
                that.autocomplete(query);
            }
        },500)
    }
}

class Default{
    constructor(){
        
    }
}