class Login{
	constructor(){
		var that = this;
		this.form = new Form();

		$('body').on('keypress',function(event){
			if(event.keyCode == 13){
				that.signin(event);
			}
		});

		$('#login-button').on('click',this.signin.bind(this));
	}
	signin(){
		var data = $('#login-form form')[0].serializeJSON();

		POST('/',{
			View:this.login.bind(this),
			data:data
		});
	}
	login(response){
		if(response.errors){
			this.form.render_errors(response.errors);
		}
		else if(response.json && response.json.next){
			$('#login-form-wrap').addClass('fadeout');
			setTimeout(function(){
				$('#login-form-wrap').remove();
			},500);

			GET(response.json.next,{
				View:function(response){
					$('body').html(response.html);
				}
			});
		}
	}
}