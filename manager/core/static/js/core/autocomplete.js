class Autocomplete{
    constructor(context){
        this.View = context.View;
        this.Model = context.Model;
        this.timeout = undefined;
        this.container = context.template;

        this.textInput = this.container.find('.name input[type="text"]')[0];

        this.textInput.on('paste keydown click',this.change.bind(this));

        if(!this.View){
            this.hiddenInput = this.container.find('.name input[type="hidden"]')[0];
            this.values = eval(this.hiddenInput.value);

            this.container.find('.remove').on('click',this.remove.bind(this));
        }

        this.values_container = this.container.find('.values')[0];
        this.result_container = this.container.find('.variants')[0];
    }
    pick(e){
        var value = parseInt(e.target.get('value'));
        var text = e.target.text();
        var item = render($('#autocompleteItem'),{value:value,text:text});

        if(Array.isArray(this.values)){
            if(this.values.includes(value)){
                this.result_container.hide();
                this.textInput.value = '';
                return;
            }

            this.values.push(parseInt(value));
            this.hiddenInput.value = JSON.stringify(this.values);

            this.values_container.append(item);
        }
        else{
            this.hiddenInput.value = this.values.toString();
            this.values_container.html(item);
        }

        this.values_container.find(`.remove[value="${value}"]`).on('click',this.remove.bind(this));

        this.result_container.hide();
        this.textInput.value = '';
    }
    remove(e){
        var value = e.target.get('value');

        if(!value){
            e.target.parent().click();
            return false;
        }

        if(Array.isArray(this.values)){
            this.values.remove(value);
        }else{
            this.values = '';
        }

        this.hiddenInput.value = this.values.toString();

        e.target.parent().remove();
    }
    change(e){
        switch(e.keyCode){
            case 13: this.press_enter(e);break;
            case 38: this.press_up(e);break;
            case 40: this.press_down(e);break;
            default: this.load(e);
        }

        e.stopPropagation();
        return false;
    }
    load(e){
        if(this.timeout)
            clearTimeout(this.timeout);

        var input = e.target;
        var that = this;
        this.timeout = setTimeout(function() {
            if(input.value && input.value.length >= 3){
                GET(`/autocomplete/${that.Model}/${input.value}`,{
                    View:function(response){
                        that.result_container.html(templates.autocomplete(response.json.items));
                        that.result_container.show();
                        that.result_container.find('div').on('click',that.View ? that.View : that.pick.bind(that));
                    },
                });
            }
        }, 500);
    }
    press_enter(e){
        var item = this.container.find('.variants .active')[0];
        if(item){
            e = {};
            e.target = item;
            this.View(e);
        }
    }
    press_down(e){
        if(!this.active){
            this.active = div.find('.variants')[0].first();
            this.active.addClass('active');
        }
        else{
            this.active.removeClass('active');
            if(this.active.next()){
                this.active = this.active.next();
            }
            else{
                this.active = div.find('.variants')[0].first();
            }
            this.active.addClass('active');
        }
    }
    press_up(e){
        if(!this.active){
            this.active = div.find('.variants')[0].last();
            this.active.addClass('active');
        }
        else{
            this.active.removeClass('active');
            if(this.active.prev()){
                this.active = this.active.prev();
            }
            else{
                this.active = div.find('.variants')[0].last();
            }
            this.active.addClass('active');
        }
    }
}