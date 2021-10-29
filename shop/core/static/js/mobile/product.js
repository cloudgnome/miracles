var rating = new Rating();

jQuery('#thumb').on('click',function(){
	var f = document.createElement('div');
	f.setAttribute('id','form');
	var div = document.createElement('div');
	var close = document.createElement('div');
	close.classList.add('close');
	div.setAttribute('id','gallery');
	for(var i of gallery){
		var img = document.createElement('img');
		img.setAttribute('src',i);
		div.appendChild(img);
	}
	f.appendChild(div);
	jQuery('body').append(f);
	jQuery('body').append(close);
	setTimeout(function(){
		jQuery('#bg').show();
		jQuery('#form').toggleClass('show');
		jQuery('.close').toggleClass('show');
	},200);
});