class AutocompleteF{
	constructor(context){
		var container = context.container;

		this.container = container;
		this.Model = context.Model;
		this.variants = container.find('.variants')[0];
		this.hidden = container.find(`input[type="hidden"]`)[0];
		this.textInput = container.find('input[type="text"]')[0];
		this.removeButton = container.find('.remove');
		this.values = container.find('.values');

		this.textInput.on('paste keypress',this.autocomplete.bind(this));
		this.removeButton.on('click',this.remove.bind(this));
	}
	press_enter(e){

	}
	autocomplete(e){
		if(e.keyCode == 13){
			this.press_enter();
			return;
		}

		if(this.timeout)
			clearTimeout(this.timeout);

		var that = this;
		that.timeout = setTimeout(function(){
			GET(`/autocomplete/${that.Model}/${e.target.value}`,{
				View:function(response){
					that.variants.html(templates.autocomplete(response.json.items));
					that.container.find(`.variant`).on('click',that.add.bind(that));
					that.variants.show();
				}
			});
		},500);

		e.stopPropagation();
		return false;
	}
	add(event){
		let id = event.target.get('value');
		let name = event.target.text();

		if(!this.hidden){
			this.textInput.value = name;
			this.variants.hide();
			return;
		}

		let value = this.hidden.value;
		if(value){
			value = eval(value);
		}

		if(Array.isArray(value)){
			value.push(parseInt(id));
			value = JSON.stringify(value);
			this.values.after(templates.autocomplete_value(id,name,this.Model.title()));
		}
		else{
			value = id.toString();
			this.values.html(templates.autocomplete_value(id,name,this.Model.title()));
		}

		this.hidden.value = value;
		this.variants.hide();
		this.textInput.value = '';

		$(`.autocomplete.${this.Model} .remove[value="${id}"]`).on('click',this.remove.bind(this));
	}
	remove(e){
		let id = parseInt(e.target.get('value'));
		if(!id){
			e.target.parent().click();
			return false;
		}
		let input = this.hidden;
		let value = input.value;

		if(value){
			value = eval(value);

			if(Array.isArray(value)){
				value.remove(id);
				value = JSON.stringify(value);
			}
			else{
				value = '';
			}

			input.value = value;
			e.target.parent().remove();
		}

		$('#save').removeAttr('disabled');
	}
}