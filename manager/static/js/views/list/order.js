class OrderList extends List{
	constructor(context){
		super(context);
		$('#tracking button').on('click',this.tracking);
		$('#sms').on('click',this.sms);
		customizeSelect('.custom-select');
	}
	sms(){
		if(confirm('Are you sure?')){
			GET('/order/mass_sms',{
				View:function(response){
					if(response.json.result)
						response.alert('SMS разошлись успешно.');
				}
			});
		}
	}
	tracking(){
		GET('/order/tracking',{
			View:function(response){
				if(response.json.items){
					var items = response.json.items;
					for(var i in items){
						var item = items[i];
						var ul = create('ul');
						ul.html(`${i}:`);
						for(var value in item){
							var li = create('li');
							li.html(`${value}: ${item[value]}`);
							ul.append(li);
						}
						$('#tracking #result')[0].append(ul);
					}
					$('#tracking #result')[0].show();
				}else{
					response.alert('Нет таких заказов.');
				}
			}
		});
	}
}