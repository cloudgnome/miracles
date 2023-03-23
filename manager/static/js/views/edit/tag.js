class Tag extends Image{
	constructor(context){
		super(context);
		this.model = 'tag';
		jQuery('.meta textarea').redactor({
				plugins: ['source'],
			});
	}
}