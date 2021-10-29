var http = new XMLHttpRequest();
http.get = function(url,custom){
	this.method = 'GET';
	this.custom = custom;
	this.url = url;
	this.request();
};
http.post = function(url,data,custom){
	this.method = 'POST';
	this.custom = custom;
	this.url = url;
	this.data = data;
	this.request();
};
http.request = function(){
	if(this.progress)
		return;
	this.open(this.method,this.url);
	if(this.method == 'POST'){
		if(this.data instanceof FormData){
			this.setRequestHeader("X-CSRFToken", );
		}
		else if(typeof this.data == 'object'){
			this.data = JSON.stringify(this.data);
			this.setRequestHeader("X-CSRFToken", csrf_token);
			this.setRequestHeader("Content-Type", "application/json");
		}
		else{
			this.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
		}
	}
	this.setRequestHeader('X-Requested-With','XMLHttpRequest');
	this.onreadystatechange = function(){
		switch(this.readyState){
			case 1: 
				$('#loading').show();
				break;
			case 4: 
				$('#loading').hide();
				if(this.status == 200){
					if(this.getResponseHeader('Content-Type') == 'application/json'){
						try{
							this.json = JSON.parse(this.responseText);
						}catch(e){
							console.log(e);
						}
					}
					if(this.custom === true){
						try{
							this.action();
						}catch(e){
							console.log(e);
						}
					}
					else{
						this.render_form();
					}
				}
				this.progress = false;
				break;
		}
	};
	this.progress = true;
	this.send(this.data);
};
http.render_form = function(){
	$('#bg').show();
	if(!window.mobile)
		$('#form').css('top', $(document).scrollTop()+25);
	$('#form').show();
	$('#form').html(this.responseText);
	$('#form').css('margin-left',$(window).width()/2 - $('#form').first().width()/2);
};
http.alert = function(title, text){
	if(!title && !text){
		title = 'Ой!';
		text = 'Что то пошло не так и кнопка не сработала. Попробуйте найти решение <a href="http://forum.igroteka.ua/ochistka-vremennyh-fajlov-v-obozrevatelebrauzere" alt="Форум Игротека">на форуме</a> или расскажите нам об этом по телефону.'
	}
	$.gritter.add({
		title: title,
		text: text,
		class_name: 'gritter-dark',
	});
};