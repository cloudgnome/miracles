class AttributeEdit extends OneToOne{
	static block = 'main';

	constructor(context){
		context.field = 'value';
		super(context);
	}
}
class Export extends Edit{
	constructor(context){
		super(context);
		this.model = 'Export';
	}
}