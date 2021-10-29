class DeliveryField{
    constructor(type,path,val,city){
        this.timeout = NaN;
        this.type = type;
        this.path = path;
        this.val = val;
        this.city = city;
        this.load();
    }
    load(){
        if(typeof this.city !== 'undefined')
            var url = `/checkout/${this.path}/${this.type}/${this.val}/${this.city}`;
        else{
            var url = `/checkout/${this.path}/${this.type}/${this.val}`;
        }

        var that = this;
        http.action = function(){
            that.render();

            $(`#id_${that.path}`).on('click',function(event){
                if(that.path == 'city' && view.delivery.departament.css('display') == 'block')
                    view.delivery.departament.hide();

                if($(`#${that.path} .variants`)[0].children.length)
                    $(`#${that.path} .variants`).show();

                event.stopPropagation();
                return false;
            });

            $(`#${that.path} .variants .variant`).on('click',that.variants.bind(that));
        };
        http.get(url);
    }
    variants(event){
        var target = event.target;
        $(`#id_${this.path}`).value = target.text();
        $(`#${this.path} .variants`).hide();
        $(`input[name="${this.path}"]`)[0].value = target.get('value');

        if(this.path == 'departament')
            return;

        view.delivery.departament.clear();
        view.delivery.departament.append(getTemplate($('#departamentTemplate')));
        view.delivery.departament.show();

        var url = `/checkout/departament/${$('#id_delivery_type').value}/${$('input[name="city"]')[0].value}`;

        this.reload(url);

        $('#id_departament').on('input paste keypress',this.input.bind(this));
    }
    input(){
        var that = this;
        if(this.timeout)
            clearTimeout(this.timeout);
        this.timeout = setTimeout(function(){
            var value = $('#id_departament').value;
            if(value && value.length > 1){
                that.departament = new DeliveryField($('#id_delivery_type').value,'departament',$('#id_departament').value,$('input[name="city"]')[0].value);
            }
        },500);
    }
    render(){
        $(`#${this.path} .variants`).show();
        $(`#${this.path} .variants`).clear();
        $(`#${this.path} .variants`).html(this.template());
        if(http.json.items.length == 1){
            var that = this;
            setTimeout(function(){
                $(`#${that.path} .variants .variant`)[0].click();
            },100);
        }
    }
    template(){
        var result = '';
        for(var item of http.json.items){
            result += `<div class="variant" value="${item.id}">${item.address}</div>`;
        }

        return result;
    }
    reload(url){
        var that = this;
        http.action = function(){
            $('#id_departament').focus();
            $('#departament .variants').show();
            $('#departament .variants').clear();

            $('#departament .variants').html(that.template());

            $('#departament .variants .variant').on('click',function(){
                $('#id_departament').value = this.text();
                $('#departament .variants').hide();
                $('input[name="departament"]')[0].value = this.get('value');
            });
            $('#id_departament').on('click',function(event){
                if($('#departament .variants')[0].children.length)
                    $('#departament .variants').show();
                event.stopPropagation();
                return false;
            });
        };
        http.get(url);
    }
}