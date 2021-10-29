jQuery('#leave-review').on('click',function(){
	if(jQuery('#review-form').css('display') == 'block' && jQuery('#review-form textarea').val() && jQuery('#review-form input').val()){
		if(jQuery('#review-form textarea').val().length > 20){
			http.action = function(){
				if(typeof http.json !== 'undefined' && http.json.result == 1){
					jQuery('#review-form').hide();
					http.alert('Спасибо за отзыв!','Он появится на сайте после модерации.');
					jQuery('#leave-review').remove();
					jQuery('#review-form').remove();
					jQuery('.bread-crumbs').after('Спасибо! Ваш отзыв появиться после модерации.');
				}
				else{
					http.alert('Форма не валидна','С полями формы что то не так.');
				}
				jQuery('#bg').hide();
			};
			http.post('/Книга_отзывов',jQuery('#review-form').serialize(),true);
		}
		else{
			jQuery('#review-form textarea').css('border','1px solid red');
			http.alert('Форма не валидна','Минимум 20 сиволов для текста отзыва.');
		}
	}
	else{
		jQuery('#review-form').show();
	}
});
jQuery('#review-form textarea').on('change',function(){
	if(jQuery(this).val().length > 20){
		jQuery(this).css('border','1px solid grey');
	}
});
jQuery('.reply').on('click',function(){
	jQuery('#review-form').show();
});