class Product extends Buy{
	constructor(){
		super();
		this.id = $('.product')[0].get('data-id');

		this.activeTab = $('.tabs label.active');
		$('.tabs label').on('click',this.tabs.bind(this));
		$('.call-back').on('click', this.callback.bind(this));

		$('#feedback-form button').on('click',this.feedback.bind(this));

		$('.quick-order').on('click',this.quickOrder.bind(this));

		this.gallery = new Gallery(gallery);

		if(pageObject.compare.includes(this.id))
			$('#product .fas.fa-balance-scale').active();
		else{
			$('#product .fas.fa-balance-scale').on('click',this.comparef.bind(this));
		}

		if(pageObject.favorite.includes(this.id))
			$('#product .fas.fa-star').active();
		else{
			$('#product .fas.fa-star').on('click',this.favoritef.bind(this));
		}

		this.rating = new Rating();
	}
	comparef(event){
		if(!pageObject.compare.includes(this.id)){
			pageObject.compare.push(this.id);
			storage.compare = JSON.stringify(pageObject.compare);
		}
		var className = event.target.classList[1];
		var target = $(`header .${className}`)[0];
		target.prev().text(pageObject.compare.length);
		target.parent().show();
		event.target.active();
		this.animate(this.getDataAnimateToHeader(target));
	}
	favoritef(event){
		if(!pageObject.favorite.includes(this.id)){
			pageObject.favorite.push(this.id);
			storage.favorite = JSON.stringify(pageObject.favorite);
		}
		var className = event.target.classList[1];
		var target = $(`header .${className}`)[0];
		target.prev().text(pageObject.favorite.length);
		target.parent().show();
		event.target.active();
		this.animate(this.getDataAnimateToHeader(target));
	}
	getDataAnimateToHeader(target){
		var img = $('#big-photo img')[0];
		var item = $('#big-photo').getBoundingClientRect();

		return [img,item,target.parent()]
	}
	getDataToAnimate(target){
		var img = $('#big-photo img')[0];
		var item = $('#big-photo').getBoundingClientRect();
		var toTarget = $('#panel .cart')[0];

		return [img,item,toTarget]
	}
	quickOrder(){
		try{
			var qty = $('#product .quantity input')[0].value;
		}catch(e){
			var qty = 1;
		}
		var that = this;
		http.action = function(){
			if(typeof http.json !== 'undefined' && typeof http.json.href !== 'undefined')
				location.href = http.json.href;
			else{
				pageObject.renderForm();
			}
			var quickOrder = new Callback(that.id,qty);
		};
		http.get(`/checkout/quick_order/${this.id}/${qty}`);

		ga('send', 'event', 'заказ 1 клик', 'отправить заказ в 1 клик', '');

		return false;
	}
	tabs(event){
		activeTab.removeClass('active');
		activeTab = this;
		this.addClass('active');
	}
	callback(){
		var that = this;
		http.action = function(){
			pageObject.renderForm();
			var callback = new Callback(that.id);
		};
		http.get(`/checkout/callback/${this.id}`);
	}
	feedback(){
		http.action = function(){
			if(http.json && http.json.result){
				var text = $('#id_text').value;
				var template = getTemplate($('#feedbackTemplate'));
				template.querySelector('h4').text(http.json.author);
				template.querySelector('p').text(text);
				$('#reviews').before(template);
				$('#feedback-form').remove();
				$('#id_text').value = '';
			}else if(http.json.authenticate){
				pageObject.user.signinForm();
			}else{
				http.alert('Странно','Мы обработали ваш запрос, но ничего не вышло.');
			}
		};
		var data = $('#feedback-form').serializeJSON();
		data['product'] = this.id;
		if(data['text'].length < 20)
			return false;
		http.post('/catalog/feedback',data);
	}
}