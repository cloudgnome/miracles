class Validator{
	constructor(form,rules){
		this.valid = [];
		this.invalid = [];
		this.form = form;
		this.rules = rules;
		this.form.validateSubmit = this.form.find('#submit');
		this.form.valid = false;

		if(this.form.validateSubmit)
			this.form.on('submit',this.submit.bind(this));

		for(let[key,rulesList] of Object.entries(rules)){
			this.listenRules(this.form.find(`[name=${key}]`)[0],rulesList);
		}
	}
	listenRules(elem,rule){
		elem.on(rule['event'] ? rule['event'] : 'paste keydown focusout',function(event){
			var elem = event.target;

			if(elem.timeout)
				clearTimeout(elem.timeout);

			if(event.type == 'focusout'){
				if(!elem.value && rule['required'])
					this.error(elem,rule['errors']['required']);
				else if(elem.invalid){
					return false;
				}
			}

			elem.removeError();
			elem.invalid = false;

			if(!event.metaKey && event.keyCode != 8 && event.keyCode != 9){
				if(rule['rules']['max_length'] && elem.value.length >= rule['rules']['max_length']){
					if(elem.selectionEnd == elem.selectionStart){
						event.stopPropagation();
						event.preventDefault();
						return false;
					}
				}
				if(event.key && rule['rules']['allow_symbols'] && !event.key.match(rule['rules']['allow_symbols'])){
					event.stopPropagation();
					event.preventDefault();
					return false;
				}
			}

			var that = this;
			elem.timeout = setTimeout(function(){
				if(!elem.value && !rule.required)
					return;
				that.cleanWhitespaces(elem);
				that.validate(elem,rule);
				if(!elem.invalid && rule['unique'])
					that.unique(elem,rule['errors']['unique']);
			},rule['timeout'] ? rule['timeout'] : 1500);

			event.stopPropagation();
			return false;
		}.bind(this));
	}
	validate(elem,rules){
		for(let[key,rule] of Object.entries(rules['rules'])){
			var result = this[key](elem,rule);
			if(result){
				this.pop(elem);
				if(rules['handler'])
					rules.handler(elem);
				if(!this.invalid.length)
					this.form.triggerValid();
			}else{
				this.error(elem,rules['errors'][key]);
			}
		}
	}
	allow_symbols(){
		return true;
	}
	is_valid(){
		for(let[key,rule] of Object.entries(this.rules)){
			var elem = this.form.find(`[name=${key}]`)[0];
			this.validate(elem,rule);
		}
		if(this.invalid.length){
			this.invalid[0].focus();
			return false;
		}else{
			return true;
		}
	}
	submit(event){
		for(let[key,rule] of Object.entries(this.rules)){
			var elem = this.form.find(`[name=${key}]`)[0];
			this.validate(elem,rule);
			if(!elem.invalid && rule['unique'])
				this.unique(elem,rule['errors']['unique']);
		}
		if(!Array.isArray($("#g-recaptcha-response")) && !$("#g-recaptcha-response").value){
			event.preventDefault();
			event.stopPropagation();
			return false;
		}

		if(this.invalid.length){
			this.invalid[0].focus();
			event.preventDefault();
			event.stopPropagation();
			return false;
		}
	}
	cleanWhitespaces(elem){
		elem.value = elem.value.replace(/(^\s+|\s+$)/g, '');
	}
	checked(elem,rule){
		if(!elem.checked)
			return false;
		return true;
	}
	radio(elem,rule){
		if(!$(`[name="${elem.name}"]:checked`)[0])
			return false;
		return true;
	}
	equal(elem,rule){
		if(elem.value != this.form.find(`[name=${rule}]`)[0].value)
			return false;
		return true;
	}
	min_length(elem,rule){
		if(elem.value.length < rule)
			return false;
		return true;
	}
	max_length(elem,rule){
		if(elem.value.length > rule)
			return false;
		return true;
	}
	min(elem,rule){
		if(elem.value < rule)
			return false;
		return true;
	}
	max(elem,rule){
		if(elem.value > rule)
			return false;
		return true;
	}
	regex(elem,rule){
		var match = elem.value.match(rule);
		if(!match)
			return false;
		return true;
	}
	unique(elem,error){
		http.action = function(){
			if(http.json && !http.json.result){
				this.error(elem,error);
				if(!this.invalid.length)
					this.form.triggerValid();
			}
		};
		http.post('/match/user',{phone:elem.value});
	}
	push(elem){
		if(!this.invalid.includes(elem))
			this.invalid.push(elem);
		if(this.valid.includes(elem))
			this.valid.pop(elem);
		elem.invalid = true;
	}
	pop(elem){
		if(!this.valid.includes(elem))
			this.valid.push(elem);
		if(this.invalid.includes(elem))
			this.invalid.pop(elem);
		elem.invalid = false;
	}
	error(elem,error){
		elem.triggerError(error);
		this.push(elem);
	}
}