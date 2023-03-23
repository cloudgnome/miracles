var timeout;
class OrderEdit extends Edit{
	constructor(context){
		super(context);
		this.model = 'order';
		this.panel = $('#sms-panel');
		this.panelButtons = $('#sms-panel .buttons');
		this.cart = new Cart(context);
		this.address = $('#id_address').value;
		this.seats = $('#seats');
		this.product_names = this.collectNames();
		this.index = 0;

		this.delivery_type = $('#id_delivery_type').value;

		this.smsButton = $('#sms');

		this.OptionsSeat = [];

		$('#add-seat').on('click',this.addSeat.bind(this));
		$('#order-ttn .close').on('click',this.createTTHwindow);

		$('#make-ttn').on('click',this.ttn.bind(this));
		this.smsButton.on('click',this.smsPanel.bind(this));
		$('#sms-panel .sel-items-wrapper > div').on('click',this.sms.bind(this));
		$('#track').on('click',this.track.bind(this));
		$('#id_delivery_type').on('change',this.delivery.bind(this));
		$('#create-ttn').on('click',this.createTTHwindow);
		$('#create-ttn *').on('click',(event) => {
			event.stopPropagation();
			return false;
		});

		$('#id_city').on('input keyup paste',this.city.bind(this));

		$('#id_departament').on('input keyup paste', () => {
			this.departament($('#id_delivery_type').value,$('input[name="city"]')[0].value);
		});

		let type = $('#id_delivery_type').value;
		if(type == 1 || type == 2){
			$('#city').show();
			$('#departament').show();
		}

		$('body').on('click',this.hide_variants);

		$('#id_city').on('click', (e) => {
			let variants = $('#city .variants')[0];
			if(e.target.value && variants.children.length)
				variants.show();
			else{
				this.city(true);
			}
			e.stopPropagation();
			return false;
		});

		$('#id_departament').on('click', (e) => {
			let variants = $('#departament .variants')[0];
			if(e.target.value && variants.children.length)
				variants.show();
			else{
				this.departament($('#id_delivery_type').value,$('input[name="city"]')[0].value);
			}
			e.stopPropagation();
			return false;
		});

		$('#copyFIO').on('click',this.copyFIO);

		customizeSelect('.custom-select');
	}
	collectNames(){
		let result = [];
		for(let i of $('#order-items .item .name')){
			result.push(i.text());
		}
		return result
	}
	calculateSeatCost(){
		let cost = this.cart.totalSum / $('#seats .seat').length;
		$('#seats input[name="cost"]').each((elem) => {
			elem.value = cost;
		});
	}
	addSeat(){
		var seat = render($('#seat'));
		this.seats.append(seat);
		this.calculateSeatCost();
		this.seats.find('.remove').on('click',this.removeSeat.bind(this));
		if(this.product_names[this.index])
			var name = this.product_names[this.index];
		else{
			var name = this.product_names[0];
		}
		$('#seats .seat input[name="description"]').last().value = name;
		$('#seats .seat input[name="weight"]').on('change',function(e){
			e.stopPropagation();
			e.preventDefault();
			return false;
		});
		$('#seats .seat input.calculate').on('change',this.calculateVolumeGeneral);
		this.index++;
	}
	calculateVolumeGeneral(){
		var res = 0;
		$('#seats .seat').each(function(seat){
			var h = seat.find('input[name="volumetricHeight"]')[0].value;
			var w = seat.find('input[name="volumetricWidth"]')[0].value;
			var l = seat.find('input[name="volumetricLength"]')[0].value;
			if(h && w && l){
				var volumeGenaral = (h * w * l) / 4000;
				res += volumeGenaral;
				seat.find('input[name="weight"]')[0].value = volumeGenaral;
			}
		});

		$('#order-ttn input[name="volume"]')[0].value = res;
	}
	removeSeat(e){
		if(e.target.parent().hasClass('remove')){
			e.target.parent().click();
			return false;
		}
		e.target.parent().remove();
		this.calculateSeatCost();
	}
	collectSeats(){
		var result = [];
		$('#seats .seat').each(function(seat){
			result.push(seat.serializeJSON());
		});
		return result;
	}
	copyFIO(){
		var fio = `${$('#id_lname').value} ${$('#id_name').value} ${$('#id_sname').value}`;
		navigator.clipboard.writeText(fio).then(function() {
			/* clipboard successfully set */
		}, function() {
			/* clipboard write failed */
		});
	}
	hide_variants(){
		if($('#id_city').value && $('#city .variants')[0].style.display == 'block')
			$('#city .variants')[0].hide();
		if($('#id_departament').value && $('#departament .variants')[0].style.display == 'block')
			$('#departament .variants')[0].hide();
	}
	createTTHwindow(event){
		$('#order-ttn').active();
		$('#bg').active();
		event.stopPropagation();
		return false;
	}
	delivery(){
		if(this.delivery_type == $('#id_delivery_type').value)
			return;

		var type = $('#id_delivery_type').value;

		$('#city').hide();
		$('#departament').hide();
		$('input[name="city"]')[0].value = '';
		$('#id_city').value = '';
		$('input[name="departament"]')[0].value = '';
		$('#id_departament').value = '';

		if(type != 3 && $('#address') && !Array.isArray($('#address')))
			$('#address').remove();

		if(type == 1 || type == 2){
			$('#city').show();
			$('#departament').show();
		}
		if(type == 3){
			var div = create('div');
			var address = templates.address();
			div.html(address);
			div.set('id','address');
			$('#order-info').afterOf(div,$('#id_payment_type').parent());
		}
	}
	city(click){
		if(timeout)
			clearTimeout(timeout);

		var type = $('#id_delivery_type').value;
		var city = $('#id_city').value;

		var that = this;
		timeout = setTimeout(() => {
			if(city && city.length > 1){
				GET(`/delivery/city/${type}/${city}`,{
					View:function(response){
						$('#city').show();
						$('#city .variants')[0].clear();
						$('#city .variants')[0].html(templates.variants(response.json));
						$('#city .variant').on('click',function(e){
							$('#id_city').value = e.target.text();
							$('input[name="city"]')[0].value = e.target.get('value');
							that.departament(type, e.target.get('value'));
						});
						for(var item of response.json){
							if(item.address == $('#id_city').value && !click){
								$('input[name="city"]')[0].value = item.id;
								that.departament(type, item.id);
								return;
							}
						}
						$('#city .variants')[0].show();
					}
				});
			}
		},500);
	}
	departament(type, city_id, value){
		if(!value)
			var value = $('#id_departament').value;

		if(timeout)
			clearTimeout(timeout);
		timeout = setTimeout(() => {
			GET(`/delivery/departament/${type}/${city_id}/${value}`,{
				View:function(response){
					$('#departament').show();
					$('#departament .variants')[0].clear();
					$('#departament .variants')[0].show();
					$('#departament .variants')[0].html(templates.variants(response.json));
					$('#departament .variant').on('click',function(e){
						$('#id_departament').value = e.target.text();
						$('input[name="departament"]')[0].value = e.target.get('value');
					});
				}
			});
		},500);
	}
	save(e){
		let items = [];

		$('#items .order-item').each(function(item){
			let qty = parseInt(item.find('input[name="qty"]')[0].value);
			let price = parseInt(item.find('input[name="price"]')[0].value);
			items.push({id:item.get('product-id'),qty:qty,price:price});
		});

		let context = {};
		context.data = $('form').serializeJSON();
		context.data.items = items;
		context.data.remove = this.cart.removeList;

		let that = this;
		context.View = function(response){
			if(response.json.result){
				that.cart.removeList = [];
				if(response.json.href){
					GET(response.json.href);
				}else{
					response.alert('Сохранен успешно.',3000);
				}
			}else if(response.json.errors){
				let errors = '';
				for(let error in response.json.errors){
					errors += error + '<br>' + response.json.errors[error] + '<br>';
				}
				errors += response.json.nonferrs + '<br>';
				response.alert(errors,7000);
			}
		};

		PUT(this.href,context);

		e.stopPropagation();
		e.preventDefault();
		return false;
	}
	ttn(e){
		let context = {data:{}};
		context.data.order = $('#order').serializeJSON();
		context.data.ttn = $('#order-ttn').serializeJSON();
		context.data.seats = this.collectSeats();
		context.data.total = $('#total .sum').text();

		context.View = function(response){
			if(response.json.ref){
				/*win = window.open("https://my.novaposhta.ua/orders/printDocument/orders[]/"+http.json.ref+"/type/html/apiKey/a5d31efa7bc0f7b138a06a130d8e5327",'_blank');
				win.focus();
				win.print();*/
				$('#id_status').value = 8;
				response.alert('TTH создана');
			}else if(response.json && response.json.errors){
				response.renderErrors();
			}
		};
		POST('/order/ttn',context);
	}
	smsPanel(event){
		this.smsButton.active();
		this.panel.active();
		this.panelButtons.active();
		event.stopPropagation();
	}
	sms(e){
		var summ = null;
		var delivery_type = $('#id_delivery_type');
		var type = e.target.get('id');

		if(delivery_type.value == 3)
			summ = prompt('Введи сумму');
		if(delivery_type.value == 3 && !summ)
			return false;

		if((type == 'ttn' && Array.isArray($('#id_ttn'))) || (type == 'ttn' && !$('#id_ttn').value.length)){
			Http.alert('Создайте ТТН');
			return;
		}

		var context = {};
		context.View = function(response){
			if(response.json.result){
				response.alert('Отправлена.');
			}
		};
		if(summ)
			GET(`/order/sms/${this.id}/${type}/${summ}`,context);
		else{
			GET(`/order/sms/${this.id}/${type}`,context);
		}
	}
	track(){
		GET(`/order/track/${this.id}`,{
			View:function(response){
				response.alert(JSON.stringify(response.json));
			}
		});
	}
}