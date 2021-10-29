class Guestbook{
	constructor(){
		$('#leave-review').on('click',this.review);

		$('#review-form textarea').on('change',function(){
			if(this.value.length > 20)
				this.css('border','1px solid grey');
		});

		$('.reply').on('click',function(){
			$('#review-form').show();
		});
	}
	review(){
		if($('#review-form').css('display') == 'block'){
			if($('#review-form textarea')[0].value.length > 20){
				http.action = function(){
					if(typeof http.json !== 'undefined' && http.json.result){
						$('#review-form').hide();
						http.alert('Спасибо за отзыв! Он появится на сайте после модерации.',7000);
						$('#leave-review').remove();
						$('#review-form').remove();
					}else if(http.json && http.json.authenticate){
						pageObject.user.signinForm();
					}else{
						http.alert('Форма не валидна' + http.json.errors);
					}
					$('#bg').hide();
				};
				http.post('/leave_review',$('#review-form').serializeJSON());
			}else{
				$('#review-form textarea').css('border','1px solid red');
				http.alert('Форма не валидна Минимум 20 сиволов для текста отзыва.');
			}
		}else{
			$('#review-form').show();
		}
	}
}