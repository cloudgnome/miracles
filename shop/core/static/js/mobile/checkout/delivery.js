class Delivery{
    constructor(){
        this.departament = $('#departament');
        this.city = $('#city');
        this.messageBox = $('#delivery_message');
        this.paymentTypeBox = $('#id_payment_type');
        this.lname = $('#id_lname');
        this.sname = $('#id_sname');
        this.paymentOptions = $('#id_payment_type option');
        this.timeout = NaN;

        this.npMessage = 'Внимание! Курьерская доставка осуществляется транспортной компанией \
            Новая Почта согласно их тарифам и по 100%й предоплате. Оплата самой доставки осуществляется \
            наличными при получении товара, курьеру Новой Почты.';
        this.prepayMessage = 'Внимание! Доставка возможна только по предоплате.';

        this.delivery_type_box = $('#id_delivery_type');
        this.delivery_type_box.on('change select',this.delivery_type.bind(this));

        var that = this;
        document.ready(function(){
            that.paymentSelect = that.paymentTypeBox.next().next();
        });
    }
    delivery_type(event){
        var target = event.target;
        var val = target.value;

        this.initials(val);

        switch(val){
            case "1": this.delivery(val); break;
            case "2": this.delivery(val); this.deliveryMessage(this.prepayMessage); break;
            case "3": this.address(); this.deliveryMessage(this.prepayMessage); break;
            case "5": this.address(); this.deliveryMessage(this.npMessage); break;
            default: this.default(); break;
        }
    }
    message(message){
        this.messageBox.show();
        this.messageBox.text(message);
    }
    address(){
        this.departament.clear();
        this.city.clear();
        this.city.append(getTemplate($('#addressTemplate')));
        this.city.show();
    }
    deliveryMessage(message){
        this.message(message);
        Select.selects['id_payment_type'].disable(0);
        Select.selects['id_payment_type'].pick(1);
    }
    initials(val){
        if(val == 4){
            this.lname.parent().hide();
            this.sname.parent().hide();
            this.lname.required = false;
        }else{
            this.lname.parent().show();
            this.sname.parent().show();
            this.lname.required = true;
        }
    }
    delivery(val){
        if(val == 1){
            this.messageBox.hide();
            Select.selects['id_payment_type'].reload();
        }

        var that = this;
        if(val == 2 || val == 1){
            this.city.clear();
            this.departament.clear();
            this.city.append(getTemplate($('#cityTemplate')));
            $('#id_city').on('input paste keypress',function(){
                if(that.timeout)
                    clearTimeout(that.timeout);
                if($('#city .variants').css('display') == 'block')
                    $('#city .variants').hide();
                that.timeout = setTimeout(function(){
                    var value = $('#id_city').value;
                    if(value && value.length > 1)
                        that.field = new DeliveryField($('#id_delivery_type').value,'city',$('#id_city').value);
                },500);
            });
        }
    }
    default(){
        this.city.clear();
        this.departament.clear();
        this.messageBox.hide();
        this.paymentOptions.removeAttr('disabled', 'disabled');
        this.paymentTypeBox.value = '';
    }
}