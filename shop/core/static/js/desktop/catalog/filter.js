class Filter{
    constructor(parameters){
        this.q = new URLSearchParams(window.location.search).get('q');
        this.form = $('#filters');
        this.min = parseInt(parameters['min']);
        this.max = parseInt(parameters['max']);
        this.page = parameters['page'];
        this.num_pages = parameters['num_pages'];

        this.slider();

        this.url = new URL(`${location.protocol}//${location.host}${location.pathname}${location.search}`);

        this.init();

        $('#filter').on('click',this.filter.bind(this));

        customizeSelect();

        addEventListener('scroll',this.scrollFilter.bind(this));
    }
    init(){
        this.ordering = this.url.searchParams.get('ordering');
        if(this.ordering)
            $('#price-sort').value = this.ordering;

        this.storage__in = this.url.searchParams.get('storage__in');
        this.storage__in = eval(this.storage__in);
        if(this.storage__in){
            this.storage__in = this.storage__in.join();
            $('#storage-filter').value = this.storage__in;
        }

        this.brand__id__in = this.url.searchParams.get('brand__id__in');
        this.brand__id__in = eval(this.brand__id__in);
        if(this.brand__id__in){
            for(var item of this.brand__id__in){
                var i = $(`input[name="brand__id__in[]"][value="${item}"]`)[0];
                if(i){
                    i.checked = true;
                }
            }
        }

        this.attributes__id = this.url.searchParams.get('attributes__id');
        this.attributes__id = eval(this.attributes__id);
        if(this.attributes__id){
            for(var item of this.attributes__id){
                $(`.attributes option[value="${item}"]`)[0].parent().value=item;
            }
        }

        if(window.and_filters){
            for(var item of and_filters){
                $('option[value="'+item[1]+'"]').parent().val(item[1]);
                $('option[value="'+item[1]+'"]').parent().selectmenu('refresh');
            }
        }
    }
    do_filter(scroll){
        if(!scroll){
            this.url.search = "";
        }

        var parameters = this.form.serializeJSON();

        if(scroll && this.page)
            parameters['page'] = this.page;

        for(var parameter of Object.keys(parameters)){
            if(typeof parameters[parameter] == 'object')
                this.url.searchParams.set(parameter,"["+parameters[parameter]+"]");
            else{
                this.url.searchParams.set(parameter,parameters[parameter]);
            }
        }

        var that = this;
        http.action = function(){
            $('.pagination').remove();
            if(scroll && that.page){
                $('#category .items').after(http.responseText);

                $('.buy').on('click',view.buy.bind(view));

                $('.quantity .minus').on('click',view.minus.bind(view));
                $('.quantity .plus').on('click',view.plus.bind(view));
                $('.quantity input').on('change',view.input.bind(view));

                that.page++;
                if(that.page > that.num_pages)
                    that.page = 0;
                else{
                    that.url.searchParams.set('page',that.page);
                }
            }
            else{
                $('#category .items').html(http.responseText);
            }
            if(!scroll && document.documentElement.clientHeight < 800)
                scrollTop();
        };

        if(this.q)
            this.url.searchParams.set('q',this.q);

        var href = this.url.pathname + this.url.search;
        if(scroll)
            http.get(href);
        else{
            location.href = `${location.protocol}//${location.host}${href}`;
        }
    }
    scrollFilter(event){
        if(document.body.clientHeight - window.scrollY - window.screen.height > 7000)
            return;

        if(!this.page)
            return;

        if(!http.progress)
            this.do_filter(true);
        event.stopPropagation();
        return false;
    }
    filter(event){
        if(!http.progress)
            this.do_filter();
        event.stopPropagation();
        return false;
    }
    slider(){
        if(this.min && this.max && (this.min < this.max)){
            var slider = $('#slider-range');
            var from = $("#amount-from");
            var to = $("#amount-to");

            noUiSlider.create(
                slider,
                {
                    start: [this.min, this.max],
                    connect: true,
                    range: {
                        'min':this.min,
                        'max':this.max
                    }
                }
            );
            slider.noUiSlider.on('update', function (values, handle) {

                var value = values[handle];

                if (handle) {
                    to.value = Math.round(value);
                } else {
                    from.value = Math.round(value);
                }
            });

            from.addEventListener('change', function () {
                html5Slider.noUiSlider.set([this.value, null]);
            });
            to.addEventListener('change', function () {
                html5Slider.noUiSlider.set([null, this.value]);
            });
        }
    }
}