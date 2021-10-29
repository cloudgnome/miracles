class Mixin{
	static inherit(..._bases)
	{
		class Classes {

			get base() { return _bases; }

			constructor(..._args)
			{
				var index = 0;

				for (let b of this.base) 
				{
					let obj = new b(_args[index++]);
					Mixin.copy(this, obj);
				}
			}
		
		}

		for (let base of _bases) 
		{
			Mixin.copy(Classes, base);
			Mixin.copy(Classes.prototype, base.prototype);
		}

		return Classes;
	}

	static copy(_target, _source) 
	{
		for (let key of Reflect.ownKeys(_source)) 
		{
			if (key !== "constructor" && key !== "prototype" && key !== "name") 
			{
				let desc = Object.getOwnPropertyDescriptor(_source, key);
				Object.defineProperty(_target, key, desc);
			}
		}
	}
}