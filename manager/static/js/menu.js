class Menu{
	constructor(parameters){
		this.container = parameters.container;
		if(Array.isArray(this.container))
			return;
		this.parameters = parameters;
		this.title = $(parameters.titleText);
		this.prevButton = $(parameters.prev);
		this.left = parameters.left ? parameters.left : 0;
		this.root = this.container;
		this.choice = parameters.choice;

		this.parameters.toggleButton.on('click touch',this.show.bind(this));
		this.container.find('div.branch').on('click touch',this.next.bind(this));
		this.prevButton.on('click touch',this.previous.bind(this));
		this.container.find('.parent.load').on('click',this.choice.bind(this));
		/*if(this.container.styles('width').includes('%')){
			this.containerWidth = window.width * (parseInt(this.container.styles('width'))/10);
		}else{
			this.containerWidth = parseInt(this.container.styles('width'));
		}*/

		this.activeMenuElement = null;
		this.init();
	}
	init(){
		this.activeMenuElement = NaN;/*$(`a.load[href="${location.pathname}"],a.load[model="${model}"]`);*/
		if(this.activeMenuElement.length){
			this.activeMenuElement.addClass('active');

			var customEvent = {};
			var parentActiveMenuElement;
			for(var item of this.activeMenuElement){
				parentActiveMenuElement = item.parent().parent();
				if(parentActiveMenuElement.hasClass('parent')){
					customEvent.target = parentActiveMenuElement;
					this.next(customEvent);
				}
			}
		}
	}
	show(event){
		if(this.active){
			this.active.removeClass('open');
			this.active = this.container.find('ul')[0].addClass('open');
		}
		this.container.css('left',`-${this.containerWidth + this.left}px`);
		this.container.show();

		var that = this;
		setTimeout(function(){
			that.container.css('left',`${that.left}px`);
		},this.parameters.delay ? this.parameters.delay : 0);
	}
	next(event){
		if(event.target.tagName == 'SPAN'){
			event.target.parent().click();
			return;
		}
		this.active = event.target.find('.sub')[0];

		var that = this;
		setTimeout(function(){
			that.active.addClass('open');
			that.title.text(event.target.find('span')[0].text());
		},this.parameters.delay ? this.parameters.delay : 0);

		this.prevButton.show('flex');

		try{
			event.stopPropagation();
			event.preventDefault();
		}catch(e){
			
		}
		return false;
	}
	previous(event){
		if(this.active == this.root)
			return;

		this.active.removeClass('open');
		this.active = this.active.parent().parent();
		this.title.text(this.active.parent().find('span')[0].text());

		var that = this;
		setTimeout(function(){
			that.active.addClass('open');
		},this.parameters.delay ? this.parameters.delay : 0);

		if(this.active == this.root){
			this.prevButton.hide();
			this.title.text('');
			return;
		}

		event.stopPropagation();
		event.preventDefault();
		return false;
	}
	close(){
		this.container.hide();
	}
}