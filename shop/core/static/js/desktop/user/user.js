class User{
    constructor(){
        $('#sign-in, .sign-in').on('click', this.signinForm.bind(this));

        $('#sign-out').on('click',this.logout.bind(this));

        var that = this;
    }
    logout(){
        http.action = function(){
            if(window.http.json && window.http.json.result == 1)
                location.reload();
        };
        http.get('/user/signout/');
    }
    signinForm(){
        var that = this;
        http.action = function(){
            if(http.json && http.json.result)
                location.reload();
            pageObject.renderForm();
            $('#login-form').on('submit',that.login.bind(that));
            $('#forget').on('click',that.forget_password.bind(that));
        };
        http.get('/user/signin/');
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
                $('#login-form').on('submit',that.login.bind(that));
                $('#forget').on('click',that.forget_password.bind(that));
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
}