storage = localStorage;
cartQty = jQuery('#cart-button span');
function clearCart(){
	storage.cart = "{}";
	storage.qty = 0;
	cartQty.text(0);
};
if(!storage.cart){
	clearCart();
}
cart = JSON.parse(storage.cart);
if(!storage.qty || storage.qty == 'NaN')
	storage.qty = Object.keys(cart).length;

cartQty.text(storage.qty);

jQuery('body').on('scroll','#form .cart',function(event){
  log(event.target);
  event.startPropagation();
});

jQuery('body').on('click', '.buy', function(){
	var cartButton = jQuery('#cart-button');
	var imgtodrag = jQuery(this).find("svg").eq(0);
	var imgclone = imgtodrag.clone()
		.offset({
		top: imgtodrag.offset().top,
		left: imgtodrag.offset().left
	})
		.css({
		'opacity': '0.5',
			'position': 'absolute',
			'height': '150px',
			'width': '150px',
			'z-index': '100'
	})
		.appendTo(jQuery('body'))
		.animate({
		'top': cartButton.offset().top + 10,
			'left': cartButton.offset().left + 10,
			'width': 75,
			'height': 75
	}, 300, 'easeInOutExpo');
	
	setTimeout(function () {
		cartButton.effect("shake", {
			times: 2
		}, 200);
	}, 1000);

	imgclone.animate({
		'width': 0,
			'height': 0
	}, function () {
		jQuery(this).detach()
	});

	var parent = jQuery(this).parent();
	var input = jQuery(this).prev().find('input').val();
	if(!input){
		parent = jQuery(this).parent().parent().parent();
		var qty = 1;
	}else{
		var qty = input ? input : 1;
	}
	if(!cart[jQuery(this).attr('value')]){
		cart[jQuery(this).attr('value')] = qty;
		cartQty.text(cartQty.text() * 1 + 1);
		storage.qty++; 
	}
	else{
		cart[jQuery(this).attr('value')] = parseInt(cart[jQuery(this).attr('value')]) + qty * 1;
	}
	storage.cart = JSON.stringify(cart);
});
function load(){
	jQuery('body').append(http.responseText);
	setTimeout(function(){
		jQuery('#bg').show();
		jQuery('#form').toggleClass('show');
		jQuery('.close').toggleClass('show');
	},200);
}
function unload(){
	setTimeout(function(){
		jQuery('.close').toggleClass('show');
		jQuery('#form').toggleClass('show');
		setTimeout(function(){
			jQuery('#form').remove();
			jQuery('.close').remove();
			jQuery('#bg').hide();
		},100);
	},100);
}
jQuery('body').on('click','.close',function(){
	setTimeout(function(){
		unload();
	},100);
	return false;
});
jQuery('#form').on('scroll',function(event){
	event.stopPropagation();
	return false;
});
jQuery('#phonesButton').on('click', function(){
	jQuery(this).next().toggle();
	return false;
});
jQuery('#cart-button').on('click',function(){
	http.action = load;
	http.post(language + '/cart/',data=cart,true);
});
jQuery('.close').on('click touch', function(event){
	unload();
	event.stopPropagation();
	return false;
});
jQuery('body').on('click','#sign-up,.sign-up',function(){
	http.get('/user/signup/');
	return false;
});
jQuery('body').on('click tap',function(){
	if(jQuery('.phones').css('display') == 'block')
		jQuery('.phones').hide();
});
jQuery(window).on('scroll',function () {
	if(jQuery(document).scrollTop() > 150){
		jQuery("#scroll-up").show();}
	else{
		jQuery("#scroll-up").hide();}
});
jQuery("#scroll-up").on('click',function(){
	jQuery("html, body").animate({ scrollTop: 0 }, 300);
});
jQuery('#bg').on('click',function(){
	if(jQuery('#filters .dropdown').css('display') == 'block'){
		jQuery('#filters .dropdown').hide();
		jQuery('#filters .dropdown').prev().hide();
	}
	unload();
});
jQuery('nav#menu ul')[0].innerHTML = user + jQuery('nav#menu ul')[0].innerHTML;
jQuery(function() {
	jQuery('nav#menu').mmenu();
	menu = jQuery("nav#menu").data( "mmenu" );
});
jQuery('#login-button,.sign-in').on('click', function(){
	http.action = load;
	http.get('/user/signin/',true);
	menu.close();
	return false;
});

jQuery('#logout').on('click',function(){
	http.action = function(){
		if(window.http.json && window.http.json.result == 1)
			location.reload();
	};
	http.get('/user/signout/',true);
});

href = new URL(location.href);
if(href.searchParams)
	q = href.searchParams.get('q');
else{
	query = getQueryParams(location.search);
	q = query.q;
}
function serializeJSON(form){
	var i, j, q = [];
	var data = {};
	for (i = form.elements.length - 1; i >= 0; i = i - 1) {
		if (form.elements[i].name === "") {
			continue;
		}
		switch (form.elements[i].nodeName) {
		case 'INPUT':
			switch (form.elements[i].type) {
			case 'text':
			case 'hidden':
			case 'password':
			case 'button':
			case 'reset':
			case 'submit':
			case 'number':
			case 'date':
				if(form.elements[i].name == 'csrfmiddlewaretoken')
					break;
				data[form.elements[i].name] = form.elements[i].value;
				break;
			case 'checkbox':
			case 'radio':
				if(form.elements[i].name.includes('[]') && form.elements[i].checked){
					name = form.elements[i].name.replace('[]','');
					if(!data[name])
						data[name] = [];
					data[name].push(form.elements[i].value);
				}
				else if(form.elements[i].checked)
					data[form.elements[i].name] = form.elements[i].value;
				break;
			case 'file':
				file = form.elements[i].files[0];
				if(file){
					data[file.name] = file;
				}
				break;
			}
			break; 
		case 'TEXTAREA':
			data[form.elements[i].name] = form.elements[i].value;
			break;
		case 'SELECT':
			switch (form.elements[i].type) {
			case 'select-one':
				if(form.elements[i].name.includes('[]') && form.elements[i].value){
					name = form.elements[i].name.replace('[]','');
					if(!data[name])
						data[name] = [];
					data[name].push(form.elements[i].value);
				}
				else if(form.elements[i].value)
					data[form.elements[i].name] = form.elements[i].value;
				break;
			case 'select-multiple':
				for (j = form.elements[i].options.length - 1; j >= 0; j = j - 1) {
					if (form.elements[i].options[j].selected) {
						data[form.elements[i].name] = form.elements[i].options[j].value;
					}
				}
				break;
			}
			break;
		case 'BUTTON':
			switch (form.elements[i].type) {
			case 'reset':
			case 'submit':
			case 'button':
				data[form.elements[i].name] = form.elements[i].value;
				break;
			}
			break;
		}
	}

	return data;
}
log = function(log){
	console.log(log);
};
history = window.history;


function navigationBack(event){
    this.parent().active();
    event.stopPropagation();
    return false;
}
function navigationMenu(event){
    log(event.target);
    if(event.target.hasClass('image') && event.target.parent().hasClass('parent') == false){
        event.target.next().click();
    }
    if(this.find('.sub')[0].hasClass('active'))
        return false;
    var sub = this.find('.sub');
    if(sub.length)
        sub[0].active();
    else{
        this.find('a')[0].click();
    }
}

jQuery('#navigation #categories > div,#navigation .children > div,#navigation .sub > .parent,#navigation .image').on('click',navigationMenu);

jQuery('#navigation .back').on('click',navigationBack);