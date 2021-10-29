class Cart{
	constructor(){
		$('#cart-form .quantity .minus').on('click',this.minus.bind(this));
		$('#cart-form .quantity .plus').on('click',this.plus.bind(this));
		$('#cart-form .quantity input').on('change',this.input.bind(this));

		$('#continue').on('click',this.continue.bind(this));
		$('#clear').on('click',this.clear.bind(this));
		$('#cart-form .remove').on('click',this.remove.bind(this));
		$('#cart-form .checkout').on('click',this.checkout.bind(this));
		this.form = $('#cart-form');
	}
	checkout(e){
		$('.checkout').active();
		$('.checkout .loading').active();

		http.action = function(){
			if(http.json && http.json.result){
				location.href = language + '/checkout/';
			}
			$('.checkout').active();
			$('.checkout .loading').active();
		};
		var data = $('#cart-form').serializeJSON();
		http.post(language + '/checkout/',data);
	}
	input(event){
		var target = event.target;
		var qty = target.value;
		var price = target.get('data-price');

		if(qty < 1 || isNaN(qty)){
			qty = 1;
			target.value = 1;
		}
		target.parent().parent().find('.total span').text(qty * price);
		this.total();
	}
	minus(event){
		var target = event.target;
		var input = target.next();
		var qty = input.value * 1 - 1;
		var productId = input.get('name');
		var price = input.get('data-price');

		if(qty > 0){
			input.set('value',qty);
			input.value = qty;
			cart[productId] = qty;
			storage.cart = JSON.stringify(cart);
			target.parent().parent().find('.total span').text((qty) * (price * 1));
			this.total();
		}
		return false;
	}
	plus(event){
		var target = event.target;
		var input = target.prev();
		var qty = input.value * 1 + 1;
		var productId = input.get('name');
		var price = input.get('data-price');

		if(qty > 1){
			input.value = qty;
			cart[productId] = qty;
			storage.cart = JSON.stringify(cart);
			target.parent().parent().find('.total span').text((qty) * (price * 1));
			this.total();
		}
	}
	remove(event){
		if(event.target.nodeName == 'I')
			var remove = event.target.parent();
		else{
			var remove = event.target;
		}

		var that = this;
		http.action = function(){
			if(http.json && http.json.result){
				delete pageObject.cart[remove.get('product-id')];

				storage.cart = JSON.stringify(pageObject.cart);
				if(storage.qty > 0){
					storage.qty = parseInt(storage.qty) - 1;
					pageObject.cartQty.text(storage.qty);
				}
				remove.parent().remove();
				if(!storage.qty || storage.qty == 0)
					that.clear(event);
				that.total();

			}
		};
		http.get(`/cart/remove/${remove.get('item-id')}/`);
	}
	clear(event){
		var that = this;
		http.action = function(){
			pageObject.renderForm();
			pageObject.clearCart();
		};
		http.get('/cart/clear/');

		event.stopPropagation();
		event.preventDefault();
		return false;
	}
	continue(event){
		$('#form').hide();
		$('#bg').hide();

		event.stopPropagation();
		event.preventDefault();
		return false;
	}
	total(){
		var summa = 0;
		$("#cart-form .productItem .total").each(function(elem){
			summa = summa + (elem.find('span').text() * 1);
		});
		$('#cart-form #sum').text(summa);
	}
}