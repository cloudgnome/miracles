class Gallery extends OneToOne{
	constructor(context){
		super(context);

		this.previewImage = $('#bigPhoto img')[0];
		this.fullSize = $('#bigPhoto');
		this.closeButton = $('#bigPhoto .close');
		this.stop = false;
		this.images = $('#gallery-items');
		$('#plus').on('click',this.add.bind(this));
		$('#images .remove').on('click',this.remove.bind(this));
		$('#images img').on('click',this.preview.bind(this));
		var that = this;

		this.removeListInput = $('#images input[name="remove_images"]')[0];
		this.removeList = JSON.parse(this.removeListInput.value);

		this.fullSize.on('click',this.next.bind(this));
		this.closeButton.on('click',this.close.bind(this));
	}
	close(e){
		this.fullSize.hide();
		$('#bg').hide();
	}
	next(e){
		
	}
	preview(e){
		if(this.stop){
			this.stop = false;
			return;
		}
		let image = e.target;
		this.previewImage.set('src',image.get('original'));
		this.fullSize.css('display','flex');
		$('#bg').show();
	}
	remove(e){
		if(e.target.tagName == 'I'){
			e.target.parent().click();
			e.stopPropagation();
			return false;
		}

		let parent = e.target.parent();
		let agree = confirm('Удалить картину?');
		let target = e.target;

		if(target.get('item-id') && agree){
			this.removeList.push(target.get('item-id'));
			this.removeListInput.value = JSON.stringify(this.removeList);
			parent.remove();
		}else if(agree)
			parent.remove();

		e.stopPropagation();
		return false
	}
	add(){
		let input = create('input');
		input.set('type','file');
		input.hide();
		this.input = input;
		this.images.append(input);
		input.on('change',this.render.bind(this));
		input.click();
	}
	render(e){
		let file = e.target.files[0];
		let reader = new FileReader();
		let that = this;

		reader.onload = function(e){
			let div = create('div');
			div.set('class','image ui-sortable-handle');
			div.html('<div class="remove"><i class="fas fa-times"></i></div>');
			div.find('.remove')[0].on('click',that.remove);
			let image = create('img');
			image.src = e.target.result;
			image.set('original',e.target.result);
			image.on('click',that.preview.bind(that));
			div.append(image);
			that.input.set('name','images');
			that.input.set('value',e.target.result);
			that.images.append(div);
		};
		reader.readAsDataURL(file);
	}
}