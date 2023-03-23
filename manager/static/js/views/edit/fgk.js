class OneToOne extends Edit{
	constructor(context){
		super(context);
		$('#fgk .remove').on('click',this.remove);
		$('#fgk input')[0].on('keypress input',this.addKey.bind(this));

		this.field = context.field;
		this.values = [];
	}
	addKey(e){
		if(e.keyCode == 13){
			var value = e.target.value;

			if(value && !this.values.includes(value)){
				this.values.push(value);

				var template = `<span class="remove"><i class="fas fa-times"></i></span> 
								<span class="tag">${value}</span>
								<input type="hidden" name="${this.field}[]" value="${value}">`;

				var div = create('div');
				div.set('class','value');
				div.html(template);
				div.find('.remove')[0].on('click',this.remove);
				$('#id_fgk_on_deck').append(div);
				e.target.value = '';
			}
		}
		e.stopPropagation();
		return false;
	}
	remove(e){
		this.parent().remove();
		$('#save').removeAttr('disabled');
	}
}