class Signup{
	constructor(){
		this.loadForm();
	}
	submit(){
		http.action = function(){
			if(http.json && http.json.href){
				$('#form').hide();
				$('#bg').hide();
				location.href = http.json.href;
			}
		};
		http.post('/user/signup/',$('#signup').serializeJSON());
		return false;
	}
	loadForm(){
		var that = this;
		http.action = function(){
			pageObject.renderForm();
			$('#signup').on('submit',that.submit);

			$('#id_phone').on('keypress', function (event) {
				var regex = new RegExp("^[a-zA-Z]+$");
				var key = String.fromCharCode(!event.charCode ? event.which : event.charCode);
				if (regex.test(key)) {
					event.preventDefault();
					return false;
				}
			});
		};
		http.get('/user/signup/');
	}
}