class Signin{
    constructor(){
        $('#signin').on('submit',this.login.bind(this));
        $('#forget').on('click',this.forget_password.bind(this));
        $('#sign-up').on('click',this.signup);
    }
    login(){
        var that = this;
        http.action = function(){
            if(http.json && http.json.result)
                location.reload();
            else if(http.json){
                social();
            }
        };
        http.post(language + '/user/signin/',$('#signin').serializeJSON());
    }
    forget_password(){
        $('#forget-password-form').show();
        $('#forget-password-form button').on('click',function(){
            http.action = function(){

            };
            http.post(language + '/user/forget-password/',$('#forget-password-form').serializeJSON());
        });
    }
    signup(){
        this.signup = new Signup();
    }
}