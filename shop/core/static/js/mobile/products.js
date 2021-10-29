jQuery('#filters label.dropdownButton').on('click',function(){
	jQuery(this).next().next().toggle();
	jQuery(this).next().show();
	jQuery('#bg').toggle();
	var closeButton = jQuery(this).next();
	setTimeout(function(){
		closeButton.toggleClass('show');
	},100);
});
jQuery('#filters .dropdown .aprove').on('click',function(event){
	jQuery(this).parent().toggle();
	filter();
	event.stopPropagation();
	return false;
});
jQuery('.closeDropdown').on('click',function(){
	var closeButton = jQuery(this);
	setTimeout(function(){
		closeButton.toggleClass('show');
		closeButton.hide();
	},100);
	jQuery(this).next().hide();
	jQuery('#bg').hide();
});
function filter(scroll){
	if(q){
		var url = new URL(location.protocol + '//' + location.host + language + '/search' + location.search);
		url.searchParams.set('q',q);
	}else{
		var url = new URL(location.protocol + '//' + location.host + location.pathname + location.search);
	}
	var h = jQuery(document).height() - jQuery(document).scrollTop() - jQuery(window).height();
	if(scroll && h > 2500)
		return;

	if(scroll && !window.page)
		return;

	var parameters = serializeJSON(jQuery('#filters')[0]);

	if(window.category__id)
		parameters['category__id'] = category__id;
	else if(window.tags__id)
		parameters['tags__id'] = tags__id;
	else if(window.brand__id)
		parameters['brand__id'] = brand__id;

	if(scroll && window.page)
		parameters['page'] = page;

	if(window.min && parameters.retail_price__gte.includes('грн.'))
		delete parameters.retail_price__gte;
	if(window.max && parameters.retail_price__lte.includes('грн.'))
		delete parameters.retail_price__lte;

	if(!Object.keys(parameters).length)
		return;

	http.action = function(){
		jQuery('.pagination').remove();
		if(scroll && window.page){
			jQuery('#category').append(http.responseText);
			url.searchParams.set('page',window.page);
		}
		else{
			jQuery('#category').html(http.responseText);
		}
		if(!scroll && document.documentElement.clientHeight < 800)
			jQuery("html, body").animate({scrollTop: 165},100);
	};

	for(parameter of Object.keys(parameters)){
		if(typeof parameters[parameter] == 'object')
			url.searchParams.set(parameter,"["+parameters[parameter]+"]");
		else{
			url.searchParams.set(parameter,parameters[parameter]);
		}
	}

	var href = url.pathname + url.search;
	if(q || scroll)
		http.get(href,true);
	else{
		location.href = href;
	}
}
jQuery(document).on('scroll',function(){
	if(!http.progress)
		filter(true);
});

if(window.min && window.max){
	var slider = jQuery('#slider-range')[0];
	var from = jQuery( "#amount-from" )[0];
	var to = jQuery( "#amount-to" )[0];

	noUiSlider.create(
		slider,
		{
			start: [window.min, window.max],
			connect: true,
			range: {
				'min':window.min,
				'max':window.max
			}
		}
	);
	slider.noUiSlider.on('update', function (values, handle) {

		var value = values[handle];

		if (handle) {
			to.value = Math.round(value);
		} else {
			from.value = Math.round(value);
		}
	});

	from.addEventListener('change', function () {
		html5Slider.noUiSlider.set([this.value, null]);
	});
	to.addEventListener('change', function () {
		html5Slider.noUiSlider.set([null, this.value]);
	});
	/*jQuery(function(){
		jQuery("#slider-range" ).slider({
			animate: 'fast',
			range: true,
			min: min,
			max: max,
			values: [ min, max ],
			slide: function( event, ui ) {
				jQuery( "#amount-from" ).val(ui.values[ 0 ]);
				jQuery( "#amount-to" ).val(ui.values[ 1 ]);
			}
		});
		jQuery( "#amount-from" ).val(jQuery( "#slider-range" ).slider( "values", 0) + ' грн.');
		jQuery( "#amount-to" ).val(jQuery( "#slider-range" ).slider( "values", 1) + ' грн.');
	});*/
}