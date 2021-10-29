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

        $('#id_delivery_type').on('change select',this.delivery_type.bind(this));
    }
    delivery_type(event){
        var target = event.target;
        var val = target.value;

        this.initials(val);
        this.paymentType(val);

        switch(val){
            case "1": this.delivery(val); break;
            case "2": this.delivery(val); break;
            case "3": this.address(); break;
            case "5": this.address();this.deliveryMessage(this.npMessage); break;
            default: this.default(); break;
        }
    }
    message(message){
        this.messageBox.show();
        $('#id_payment_type option[value="1"]')[0].set('disabled','disabled');
    }
    address(){
        this.departament.clear();
        this.city.clear();
        this.city.append(getTemplate($('#addressTemplate')));
        this.city.show();
    }
    deliveryMessage(message){
        this.paymentTypeBox.value = '2';
        this.message(message);
        $('#id_payment_type option[value="1"]')[0].set('disabled','disabled');
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
    paymentType(val){
        if(val == 2 || val == 3){
            this.paymentTypeBox.value = '2';
            this.message(this.prepayMessage);
        }
    }
    delivery(val){
        if(val == 1){
            this.messageBox.hide();
            this.paymentTypeBox.value = '';
            this.paymentOptions.removeAttr('disabled', 'disabled');
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