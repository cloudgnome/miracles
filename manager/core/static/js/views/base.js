class SimpleView{
	static block = 'main';

	constructor(context){
		this.deleteButton = $('#delete');

		document.ready(() => {
			$('a').on('click',Http.click);

			var menuParams = {
				container: $('#menu'),
				titleText: '#menu-title-text',
				prev: '#prev',
				delay: 0,
				toggleButton: $('#toggleMenu'),
				left: 0,
				choice:function(e){
					if(e.target.tagName == 'SPAN'){
						e.target.parent().click();
						return;
					}
					location.href = e.target.get('href');
					$('#search-text').set('model',e.target.get('model'));
					e.stopPropagation();
					e.preventDefault();
					return false;
				}
			};
			this.menu = new Menu(menuParams);

			$('.burger').on('click',function(e){
				$('menu').active();
				$('#right').toggleClass('full');

				e.stopPropagation();
				return false;
			});
		});

		$('#shop').on('click',function(){
			location.href = this.href;
		});

		$('#signout').on('click',function(){
			location.href = this.href;
		});

		if(!context)
			return;

		this.context = context;

		$(`${this.block} a`).on('click',Http.click);

		document.title = context.title;

		try{
			this.Model = context.Model ? context.Model : context.context.Model;
		}catch(e){}
	}
}

class BaseView extends SimpleView{
	constructor(context){
		super(context);

		if(!storage.theme)
			storage.theme = 'black';

		if(!storage.LANG_ORDER)
			storage.LANG_ORDER = '[]';

		$('header').set('class',storage.theme);

		$('#theme .color').on('click',function(event){
			theme(this.get('color'));
		});

		$('#nav,#nav *').on('click',function(e){
			e.stopPropagation();
			return false;
		});

		$('body').on('click',function(e){
			$('#panel-menu').removeClass('active');
			$('#panel #filter').removeClass('active');
			$('#panel #edit').removeClass('active');
			$('#left #nav.active').removeClass('active');
			$('#product-info').removeClass('active');
			$('#right').removeClass('full');
			$('#filters').removeClass('active');
		});
	}
	toString(){
		return this.__proto__.constructor.name;
	}
	change_theme(color){
		storage.theme = color;
		$('header').set('class',color);
	}
}