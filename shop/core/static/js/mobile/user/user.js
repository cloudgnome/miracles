class User{
    constructor(){
        $('#sign-in, .sign-in, #login-button').on('click', this.signinForm.bind(this));

        $('#sign-out').on('click',this.logout.bind(this));

        var that = this;
    }
    signupForm(){
        this.signup = new Signup();
    }
    logout(){
        http.action = function(){
            if(window.http.json && window.http.json.result == 1)
                location.reload();
        };
        http.get(language + '/user/signout/');
    }
    signinForm(){
        var that = this;
        http.action = function(){
            if(http.json && http.json.result)
                location.reload();
            pageObject.renderForm();
            $('#signin').on('submit',that.login.bind(that));
            $('#forget').on('click',that.forget_password.bind(that));
            $('#sign-up').on('click',that.signupForm.bind(that));
        };
        http.get(language + '/user/signin/');
        return false;
    }
    login(){
        var that = this;
        http.action = function(){
            if(http.json && http.json.result)
                location.reload();
            else if(http.json){
                social();
            }
            else{
                pageObject.renderForm();
                $('#signin').on('submit',that.login.bind(that));
                $('#forget').on('click',that.forget_password.bind(that));
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
}