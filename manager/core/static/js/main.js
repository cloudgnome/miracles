function theme(color){
	storage.theme = color;
	$('header').set('class',color);
}
/*if(window.model){
	current = $(`menu a[model="${model}"]`)[0];
	current.active();
	current.parent().active();
	current.parent().parent().active();
}*/

if(!storage.theme)
	storage.theme = 'black';

if(storage.activeMenu){
	$('menu').active();
	$('#right').toggleClass('full');
}
if(storage.activePanel && !Array.isArray($('#toggle-panel'))){
	$('#panel-wrapper').active();
	$('#toggle-panel').active();
	$('#panel-shortcuts').active();
}

$('header').set('class',storage.theme);

$('#theme .color').on('click',function(event){
	theme(this.get('color'));
});

$('#shop').on('click',function(){
	location.href = this.href;
});

$('#signout').on('click',function(){
	location.href = this.href;
});

$('body').on('click',function(){
	var filters = $('#filters');
	if(filters.style && filters.style.display == 'grid'){
		filters.hide();
	}
	/*if(window.panel && panel.className.includes('active')){
		panel.active();
		panel_buttons.active();
	}*/
});

jQuery(document).ready(function(){
	try{
		for(key of view.url.searchParams.entries()){
			if($(`#filters #${key[0]}`).length)
				$(`#filters #${key[0]}`)[0].value = key[1];
		}
	}catch(e){}
});


timeout = false;

function changeDatabase(database,url){
	http.action = function(){
		storage.database = JSON.stringify({'database':database,'url':url});
		location.reload(true);
	};
	http.get('/change_database?database='+database);
}

$('.change-database select').on('change select',function(){
	changeDatabase(this.get('database'),this.get('url'));
});

$('.change-database.logo #active').on('click',function(){
	$('.change-database.logo #sites').toggleClass('active');
});
$('.change-database.logo .database').on('click',function(){
	$('.change-database.logo #active').html(this.html());
	$('.change-database.logo #sites').toggleClass('active');
	var target = this;
	setTimeout(function(){
		changeDatabase(target.get('database'),target.get('url'));
	},500);
});

$('.burger').on('click',function(){
	if(!storage.activeMenu)
		storage.activeMenu = 1;
	else{
		storage.activeMenu = '';
	}
	$('menu').active();
	$('#right').toggleClass('full');
});

$('#search i').on('click',function(){
	setTimeout(function(){
		$('#search i').active();
		$('#search-text').active();
	},300);
});

$('#toggle-panel').on('click',function(){
	if(!storage.activePanel)
		storage.activePanel = 1;
	else{
		storage.activePanel = '';
	}
	$('#panel-wrapper').active();
	$('#panel-shortcuts').active();
	this.active();
});