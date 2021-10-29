class Form{
    constructor(){

    }
    render_errors(errors){
        for(var name of Object.keys(errors)){
            try{
                var field = $(`form input[name="${name}"]`)[0];
                var errorsBlock = field.parent().find('.errors')[0];
                errorsBlock.html(errors[name][0]);
                errorsBlock.show();
            }catch(e){
                log(e);
            }
        }
    }
}