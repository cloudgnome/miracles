class SimpleImage{
	constructor({data}){
		this.data = data;
	}
	static get toolbox(){
		return {
			title: 'Add Image',
			icon: '<i class="far fa-image"></i>'
		}
	}
	render(){
		const img = create('img');

		img.src = this.data && this.data.src ? this.data.src : '';
		return img;
	}
	save(blockContent){
		const img = blockContent.query('img');

		return {
			src: img.src
		}
	}
	load(){
		const file = e.target.files[0];
		const reader = new FileReader();
		const that = this;

		reader.onload = function(e){
			let img = create('img');
			this.data.src = e.target.result;
			this.render();
		};
		reader.readAsDataURL(file);
	}
}