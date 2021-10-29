class Profile{
    constructor(){
        this.button = $('#change-order');
        $('#orderForm').each(function(elem){
            this.change(elem)
        }.bind(this));
    }
    change(elem){
        elem.on('change input paste',function(){
            this.button.removeAttr('disabled');
            this.button.addClass('blue');
        }.bind(this));
    }
}


