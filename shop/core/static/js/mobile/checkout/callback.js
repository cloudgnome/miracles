class Callback{
    constructor(id){
        this.id = id ? id : "";

        try{
            $('#id_phone').focus();
            $('#id_phone').on('keypress', this.keypress.bind(this));
            $('#quickOrderForm').on('submit',this.submit.bind(this));
        }catch(e){

        }
    }
    keypress(event){
        var regex = new RegExp("^[a-zA-Z]+$");
        var key = String.fromCharCode(!event.charCode ? event.which : event.charCode);
        if (regex.test(key)) {
            event.preventDefault();
            return false;
        }
    }
    submit(event){
        var that = this;
        var target = event.target;
        http.action = function(){
            pageObject.renderForm();
            try{
                $('#id_phone').focus();
                $('#quickOrderForm').on('submit',that.submit.bind(that));
            }catch(e){
                ga('send', 'event', 'перезвонить', 'отправить перезвонить ', '');
            }
        };
        http.post(`${language}/checkout/callback/` + this.id,target.serializeJSON());
    }
}