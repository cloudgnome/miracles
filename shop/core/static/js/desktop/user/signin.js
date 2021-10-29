class Signin{
    constructor(){
        $('#login-form').on('submit',this.login.bind(this));
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
        http.post('/user/signin/',$('#login-form').serializeJSON());
    }
    forget_password(){
        $('#forget-password-form').show();
        $('#login-form').hide();
        $('#forget-password-form button').on('click',function(){
            http.action = function(){

            };
            http.post('/user/forget-password/',$('#forget-password-form').serializeJSON());
        });
    }
    signup(){
        this.signup = new Signup();
    }
}