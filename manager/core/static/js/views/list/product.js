var timeout;
class BaseProductList extends List{
	constructor(context){
		super(context);

		$('.availability .bool').on('click',this.availability.bind(this));

		$('.settings-button').on('click',this.addInfo.bind(this));

		this.editors = {};
	}
	availability(e){
		var availability = e.target.hasClass('true') ? true : false;
		var product_id = e.target.closer('.settings-button').get('product-id');

		POST(`/action/${product_id}/availability`,{
			data:{'availability':!availability},
			View:function(response){
				if(response.json && response.json.result){
					e.target.removeClass(availability.toString());
					availability = !availability;
					e.target.addClass(availability.toString());
				}
			}
		});
	}
	addInfo(e){
		var target = e.target;
		var productId = target.get('product-id');
		if(!productId){
			target.parent().click();
			return false;
		}
		target.active();

		this.productId = productId;
		this.targetWindow = target;

		GET(`/api/Product/${productId}/?format=json`,{
			View:this.product_info.bind(this),
		});
	}
	product_info(response){
		$('#panel-menu').active();
		$('#product-info').active();
		$('#filters').removeClass('active');
		$('.edit-action').removeClass('active');
		$('#product-info').set('product-id',this.productId);
		this.targetWindow.active();

		if(!Object.keys(this.editors).length){
			$('#panel textarea').each((elem) => {
				let id = elem.parent().parent().parent().get('type');

				elem.hide();
				elem.parent().after(`<div id="editorjs-${id}"></div>`);

				let textarea = $(`#panel .export[type="${id}"] textarea[name="${elem.name}"]`)[0];

				let dummyDiv = create('div');
				dummyDiv.html(elem.innerHTML);

				if(!dummyDiv.children && elem.innerHTML){
					let p = create('p');
					p.html(elem.innerHTML);
					dummyDiv.append(p);
				}

				let parser = edjsHTML();

				let editor = new EditorJS({
					holder: `editorjs-${id}`,
					tools: {
						header: {
							class: Header,
							inlineToolbar: ['marker', 'link'],
							config: {
								placeholder: 'Header'
							},
							shortcut: 'CMD+SHIFT+H'
						},
						image: {
							class: SimpleImage,
							inlineToolbar: true
						},

						list: {
							class: List,
							inlineToolbar: true,
							shortcut: 'CMD+SHIFT+L'
						},

						checklist: {
							class: Checklist,
							inlineToolbar: true,
						},

						quote: {
							class: Quote,
							inlineToolbar: true,
							config: {
							quotePlaceholder: 'Enter a quote',
							captionPlaceholder: 'Quote\'s author',
							},
							shortcut: 'CMD+SHIFT+O'
						},

						warning: Warning,

						marker: {
							class: Marker,
							shortcut: 'CMD+SHIFT+M'
						},

						code: {
							class: CodeTool,
							shortcut: 'CMD+SHIFT+C'
						},

						delimiter: Delimiter,

						inlineCode: {
							class: InlineCode,
							shortcut: 'CMD+SHIFT+C'
						},

						linkTool: LinkTool,

						embed: Embed,

						table: {
							class: Table,
							inlineToolbar: true,
							shortcut: 'CMD+ALT+T'
						},
					},
					data: {
						blocks: toJson(dummyDiv),
					},
					placeholder: elem.placeholder,
					onChange: (editor) => {
						editor.saver.save().then((out) => {

							let html = parser.parse(out);

							let result = '';
							if(Array.isArray(html)){
								for(let i of html){
									result += i;
								}
								html = result;
							}

							textarea.innerHTML = html;
							textarea.value = html;
						});
					},
					onReady: (e)=>{this.load_editor(response)}
				});

				this.editors[id] = editor;
			});
		}else{
			this.load_editor(response);
		}
	}
	load_editor(response){
		$(`.export input[type='radio']`).each((elem) => {elem.checked = false});
		for(let exp of response.json.export_status){
			$(`.export[type='${exp.export_id}'] [value='${exp.load}']`)[0].checked = true;
			if(exp.meta){
				let editor = this.editors[exp.export_id];

				$(`.export[type='${exp.export_id}'] [name='name']`)[0].value = exp.meta.name;
				$(`.export[type='${exp.export_id}'] [name='text']`)[0].innerHTML = exp.meta.text;

				let dummyDiv = create('div');
				dummyDiv.html(exp.meta.text);

				if(!dummyDiv.children.length && exp.meta.text){
					let p = create('p');
					p.html(exp.meta.text);
					dummyDiv.append(p);
				}

				editor.blocks.clear();
				for(let block of toJson(dummyDiv)){
					editor.blocks.insert(block.type,block.data);
				}
			}
		}
	}
}

class ProductList extends BaseProductList{
	static limit = parseInt((window.screen.availHeight - (95 + 91)) / 88) * 2;

	constructor(context){
		super(context);

		this.min = context.min_price;
		this.max = context.max_price;

		$('.autocomplete').each(function(elem){
			new AutocompleteF({container:elem,Model:elem.get('model')});
		});

		$(`.export input[type="radio"]`).on('change',this.productExport.bind(this));

		customizeSelect('.custom-select');

		this.url.searchParams.set('limit',this.limit);
		this.slider();
	}
	productExport(e){
		let target = e.target;
		let export_id = target.name;
		let value = target.value;
		let productId = $('#product-info').get('product-id');

		POST(`/Product/${productId}`,{
			data:{
				export_status:[{
					export_id:parseInt(export_id),
					load:eval(value)
				}],
			}
		});
	}
	slider(){
		if(this.min && this.max && (this.min < this.max)){
			var slider = $('#slider-range');
			var from = $("#amount-from");
			var to = $("#amount-to");
			$('#range-1').show();

			noUiSlider.create(
				slider,
				{
					start: [this.min, this.max],
					connect: true,
					step: 5,
					range: {
						'min':this.min,
						'max':this.max
					}
				}
			);
			slider.noUiSlider.on('update', (values, handle) => {

				let value = values[handle];

				if (handle) {
					to.value = Math.round(value);
				} else {
					from.value = Math.round(value);
				}

			});

			slider.noUiSlider.on('change', (values, handle) => {

				this.filter();

			});
		}
	}
}

class ProductReloadList extends ReloadList{
	static limit = parseInt(window.screen.availHeight / 1.80 / 79) * 2;

	constructor(context){
		super(context);
	}
}