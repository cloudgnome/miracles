templates = {
	autocomplete: function(items){
		result = '';
		for(item of items){
			result += `<div class="variant" value="${item.id}">
				${item.name}
			</div>`;
		}
		return result;
	},
	autocomplete_value: function(id,name,Model){
		return `<div class="value">
			<div class="remove" value="${id}"><i class="fas fa-times"></i></div>
			<a href="/${Model}/${id}">${name}</a>
		</div>`;
	},
	address: function(){
		if(view.address)
			return `<input type="text" name="address" value="${view.address}" placeholder="Адрес" id="id_address">`;
		else{
			return `<input type="text" name="address" value="" placeholder="Адрес" id="id_address">`;
		}
	},
	variants: function(items){
		result = '';
		for(item of items){
			result += `<div class="variant" value="${item.id}">${item.address}</div>`;
		}
		return result;
	},
	departaments: function(items,type){
		options = '<option value="-----" selected disabled>-----</option>';
		for(item in items){
			options += `<option value="${item}">${items[item]}</option>`;
		}
		return `<select autocomplete="off" id="id_${type}" name="${type}">${options}</select>`;
	},
	add: function(item){
		return `
				<div class="remove-wrap">
					<div class="remove" item-id=${item.get('item-id')}><i class="fas fa-times"></i></div>
				</div>
				<div class="image">
				</div>
				<div class="name">
					<a href="http://${BASE_URL}/${item.get('href')}" target="_blank">${item.text()}</a>
				</div>
				<div>
					<input type="text" name="qty" value="1">
				</div>
				<div>
					<input type="text" name="price" opt="${item.get('opt')}" value="${item.get('price')}">
				</div>
				<div class="total">${item.get('price')} грн.</div>
				<div class="store">${item.get('storage')}</div>
				<div>${item.get('qty')}шт.</div>
			`;
	},
	product: function(json){
			return `
				<div class="remove-wrap">
					<div class="remove" item-id="${json.id}"><i class="fas fa-times"></i></div>
				</div>
				<div class="name">
					<a href="http://${BASE_URL}/${json.slug}" target="_blank">${json.name}</a>
				</div>
				<div>
					<input type="text" name="qty" value="1">
				</div>
				<div>
					<input type="text" name="price" value="${json.price}">
				</div>
				<div class="total">${json.total} грн.</div>
				<div class="storage">${json.storage}</div>
				`;
		}
	};