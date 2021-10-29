try{
	jQuery = $;
}catch(e){
	console.log('jQuery doesnot exist');
}
var $ = function (selector) {
	if(selector.includes('#') && (!selector.includes(' ') || selector.includes(','))){
		var item = document.querySelector(selector);
		if(item){
			return item;
		}
		else{
			return [];
		}
	}
	else{
		return Array.prototype.slice.call(document.querySelectorAll(selector));
	}
};
HTMLCollection.prototype.toArray = function(array){
	if(!array)
		array = [];
	for(item of this){
		array.push(item);
		if(item.children.length)
			array = item.children.toArray(array);
	}
	return array;
};
Element.prototype.styles = function(property){
	return window.getComputedStyle($('#menu'))[property];
};
Element.prototype.includes = function(target){
	if(this.children.toArray().includes(target))
		return true;
	else{
		return false;
	}
};
String.prototype.title = function() {
	return this.charAt(0).toUpperCase() + this.slice(1);
};
create = function(element){
	return document.createElement(element);
};
log = function(log){
	console.log(log);
};
window.width = window.innerWidth;
Element.prototype.grid = function(){
	this.style.display = 'grid';
};
Element.prototype.next = function(){
	return this.nextElementSibling;
};
Element.prototype.prev = function(){
	return this.previousElementSibling;
};
Element.prototype.last = function(){
	return this.lastElementChild;
};
Element.prototype.active = function(){
	if(this.className.includes('active')){
		this.removeClass('active');
	}else{
		this.addClass('active');
	}
};
Element.prototype.toggleMenu = function(parameters){
	var item = this;
	var timeout = setTimeout(function(){
		item.active();
		if(parameters.parent){
			if(parameters.parent.activeItem == item){
				parameters.parent.activeItem = undefined;
				return;
			}
			if(parameters.closeAll && parameters.parent.activeItem)
				parameters.parent.activeItem.active();
			parameters.parent.activeItem = item;
		}
	},parameters.timeout ? parameters.timeout : 0);
};
Element.prototype.parent = function(){
	return this.parentElement;
};
Element.prototype.find = function(selector){
	try{
		if(selector.includes('#') && (!selector.includes(' ') || selector.includes(','))){
			return this.querySelector(selector);
		}else{
			return Array.prototype.slice.call(this.querySelectorAll(selector));
		}
	}catch(e){
		log(e);
	}
};
Element.prototype.replace = function(n,o){
	this.replaceChild(n,o);
};
Element.prototype.append = function(child){
	if(child){this.appendChild(child);}
};
Element.prototype.before = function(child,before){
	if(child){
		if(!before)
			before = this.childNodes[0];
		else{
			before = this.childNodes[before];
		}
		this.insertBefore(child,before);
	}
};
Element.prototype.getBefore = function(){
	return window.getComputedStyle(this, ':before');
};
Element.prototype.clear = function(){
	while(this.firstChild){
		this.removeChild(this.firstChild);
	}
};
Element.prototype.each = function(func){
	for(i=0;i<this.children.length;i++){
		func(this.children[i]);
	}
};
async function eachAsync(func,asyncFunc){
	this.forEach(item => {
		func(item);
	});
	await asyncFunc();
};
Element.prototype.eachAsync = eachAsync;
Element.prototype.attr = function(name){
	return this.getAttribute(name);
};
Element.prototype.get = function(name){
	return this.getAttribute(name);
};
Element.prototype.set = function(name,value){
	return this.setAttribute(name,value);
};
Element.prototype.removeAttr = function(name){
	return this.removeAttribute(name);
};
Element.prototype.html = function(html){
	if(html)
		this.innerHTML = html;
	else{
		return this.innerHTML;
	}
};
Element.prototype.after = function(html){
	this.innerHTML += html;
};
Element.prototype.afterOf = function(newElem,node){
	this.insertBefore(newElem,node);
};
Element.prototype.first = function(){
	return this.firstElementChild;
};
Element.prototype.show = function(type){
	if(type)
		this.style.display = type;
	else{
		this.style.display = 'block';
	}
};
Element.prototype.hide = function(){
	this.style.display = 'none';
};
Element.prototype.toggle = function(type){
	if(this.style.display == 'none' || this.style.display == ''){
		if(type)
			this.style.display = type;
		else{
			this.style.display = 'block';
		}
	}else{
		this.style.display = 'none';
	}
};
Element.prototype.addClass = function(name){
	this.classList.add(name);
};
Element.prototype.removeClass = function(name){
	this.classList.remove(name);
};
Element.prototype.hasClass = function(name){
	if(this.className.includes(name))
		return true;
	else{
		return false
	}
};
Element.prototype.toggleClass = function(name){
	if(this.hasClass(name))
		this.removeClass(name);
	else{
		this.addClass(name);
	}
};
Element.prototype.on = function(events,listener){
	events = events.split(' ');
	for(event in events){
		this.addEventListener(events[event],listener);
	}
};
Element.prototype.removeEvent = function(events,listener){
	events = events.split(' ');
	for(event in events){
		this.removeEventListener(events[event],listener);
	}
};
Element.prototype.switchClass = function(class1,class2){
	if(this.hasClass(class1)){
		this.removeClass(class1);
		this.addClass(class2);
	}else if(this.hasClass(class2)){
		this.removeClass(class2);
		this.addClass(class1);
	}
};
Array.prototype.switchClass = function(class1,class2){
	this.forEach(function(elem){
		if(elem.hasClass(class1)){
			elem.removeClass(class1);
			elem.addClass(class2);
		}else if(elem.hasClass(class2)){
			elem.removeClass(class2);
			elem.addClass(class1);
		}
	});
};
Array.prototype.each = function(func){
	for(i=0;i < this.length;i++){
		func(this[i]);
	}
};
Array.prototype.toggle = function(type){
	this.forEach(function(elem){
		if(elem.style.display == 'none' || elem.style.display == ''){
			if(type)
				elem.style.display = type;
			else{
				elem.style.display = 'block';
			}
		}else{
			elem.style.display = 'none';
		}
	});
};
Array.prototype.next = function(){
	return this[0].nextElementSibling;
};
Array.prototype.on = function(event,listener,selector){
	events = event.split(' ');
	this.forEach(function(elem){
		for(event in events){
			elem.addEventListener(events[event],listener);
		}
	});
};
Array.prototype.removeEvent = function(event,listener,selector){
	events = event.split(' ');
	this.forEach(function(elem){
		for(event in events){
			elem.removeEventListener(events[event],listener);
		}
	});
};
Array.prototype.after = function(html){
	this.forEach(function(elem){
		elem.innerHTML += html;
	});
};
Array.prototype.toggleClass = function(name){
	this.forEach(function(elem){
		if(elem.hasClass(name))
			elem.removeClass(name);
		else{
			elem.addClass(name);
		}
	});
};
Array.prototype.show = function(type){
	if(type)
		this.forEach(function(elem){
			elem.style.display = type;
		});
	else{
		this.forEach(function(elem){
			elem.style.display = 'block';
		});
	}
};
Array.prototype.hide = function(){
	this.forEach(function(elem){
		elem.style.display = 'none';
	});
};
Array.prototype.clear = function(){
	this.forEach(function(elem){
		while(elem.firstChild){
			elem.removeChild(elem.firstChild);
		}
	});
};
Array.prototype.append = function(child){
	this.forEach(function(elem){
		elem.append(child)
	});
};
Array.prototype.active = function(){
	this.forEach(function(elem){
		if(elem.className.includes('active')){
			elem.removeClass('active');
		}else{
			elem.addClass('active');
		}
	});
};
Array.prototype.addClass = function(name){
	this.forEach(function(elem){
		elem.classList.add(name);
	});
};
Array.prototype.removeClass = function(name){
	this.forEach(function(elem){
		if(elem.className.includes(name))
			elem.removeClass(name);
	});
};
Array.prototype.before = function(child,before){
	this.forEach(function(elem){
		if(!before)
			before = elem.childNodes[0];
		else{
			before = elem.childNodes[before];
		}
		elem.insertBefore(child,before)
	});
};
Array.prototype.hasClass = function(name){
	if(this[0].className.includes(name))
		return true;
	else{
		return false
	}
};
Array.prototype.html = function(html){
	if(html){
		this.forEach(function(elem){
			elem.innerHTML = html;
		});
	}else{
		return this[0].innerHTML;
	}
};
Array.prototype.set = function(name,value){
	this.forEach(function(elem){
		elem.setAttribute(name,value);
	});
};
Array.prototype.css = function(attr,value){
	this.forEach(function(elem){
		if(value)
			elem.style[attr] = value;
	});
};
Array.prototype.text = function(text){
	if(text){
		try{
			this[0].firstChild.nodeValue = text;
		}catch(e){
			t = document.createTextNode(text);
			this.append(t);
		}
	}
	else{
		try{
			return this[0].firstChild.nodeValue;
		}catch(e){
			return undefined;
		}
	}
};
Array.prototype.width = function(){
	return this[0].clientWidth;
};
Array.prototype.height = function(){
	return this[0].clientHeight;
};
Element.prototype.height = function(){
	return this.clientHeight;
};
Element.prototype.text = function(text){
	if(text){
		try{
			this.firstChild.nodeValue = text;
		}catch(e){
			t = document.createTextNode(text);
			this.append(t);
		}
	}
	else{
		return this.innerText;
	}
};
Element.prototype.width = function(){
	return this.clientWidth;
};
Element.prototype.top = function(value){
	this.style['top'] = value;
};
Element.prototype.enable = function(){
	this.removeAttr('disabled');
};
Element.prototype.disable = function(){
	this.set('disabled','');
};
HTMLElement.prototype.css = function(attr,value){
	if(value)
		this.style[attr] = value;
	else{
		return this.style[attr];
	}
};
Element.prototype.triggerError = function(message){
	this.addClass('invalid');
	var errorBlock = this.next();
	if(!errorBlock.hasClass('errors')){
		errorBlock = $(`.${this.name}.errors`)[0];
	}
	if(errorBlock){
		errorBlock.html(message);
		errorBlock.show();
	}
	if(this.form)
		this.form.triggerInvalid();
};
Element.prototype.removeError = function(){
	this.removeClass('invalid');
	var errorBlock = this.next();
	if(!errorBlock.hasClass('errors')){
		errorBlock = $(`.${this.name}.errors`)[0];
	}
	if(errorBlock)
		errorBlock.hide();
};
HTMLFormElement.prototype.triggerInvalid = function(){
	this.addClass('invalid');
	if(this.validateSubmit){
		this.validateSubmit.addClass('disabled');
		this.validateSubmit.set('disabled','disabled');
	}
};
HTMLFormElement.prototype.triggerValid = function(){
	this.removeClass('invalid');
	if(this.validateSubmit){
		this.validateSubmit.removeClass('disabled');
		this.validateSubmit.removeAttr('disabled');
	}
};
Element.prototype.triggerInvalid = function(){
	this.addClass('invalid');
	if(this.validateSubmit){
		this.validateSubmit.addClass('disabled');
		this.validateSubmit.set('disabled','disabled');
	}
};
Element.prototype.triggerValid = function(){
	this.removeClass('invalid');
	if(this.validateSubmit){
		this.validateSubmit.removeClass('disabled');
		this.validateSubmit.removeAttr('disabled');
	}
};
Element.prototype.validate = function(rules){
	validator = new Validator(this,rules);
};
Array.prototype.ready = function(func){
	this.forEach(function(elem){
		elem.onload = func;
	});
};
Element.prototype.ready = function(func){
	this.onload = func;
};
Array.prototype.remove = function(val) {
	this.splice(this.indexOf(val),1);
};
Array.prototype.last = function(){
	return this[this.length - 1];
};
Element.prototype.serializeJSON = function(){
	var data = {};
	for(var i of ['input','select','textarea']){
		for(var elem of this.find(i)){
			switch(elem.type){
				case 'text':
				case 'hidden':
				case 'password':
				case 'button':
				case 'reset':
				case 'submit':
				case 'number':
				case 'date':
					if(elem.value)
						data[elem.name] = elem.value;
					break;
				case 'checkbox':
				case 'radio':
					if (elem.checked) 
						data[elem.name] = elem.value;
					break;
				case 'select-one':
					if(elem.value)
						data[elem.name] = elem.value;
					break;
				case 'select-multiple':
					data[elem.name] = [];
					for (var j = elem.options.length - 1; j >= 0; j = j - 1){
						if (elem.options[j].selected)
							data[elem.name].append(elem.options[j].value);
					}
					break;
			}
		}
	}

	return data;
};
function serialize(){
	var i, j, q = [];
	var data = new FormData();
	for (i = this.elements.length - 1; i >= 0; i = i - 1) {
		if (this.elements[i].name === "") {
			continue;
		}
		switch (this.elements[i].nodeName) {
		case 'INPUT':
			switch (this.elements[i].type) {
			case 'text':
			case 'hidden':
			case 'password':
			case 'button':
			case 'reset':
			case 'submit':
			case 'number':
			case 'date':
				if(this.elements[i].value)
					data.append(this.elements[i].name, this.elements[i].value);
				break;
			case 'checkbox':
			case 'radio':
				if (this.elements[i].checked) {
					data.append(this.elements[i].name, this.elements[i].value);
				}
				break;
			case 'file':
				file = this.elements[i].files[0];
				if(file){
					data.append(file.name, file);
				}
				break;
			}
			break; 
		case 'TEXTAREA':
			if(this.elements[i].value)
				data.append(this.elements[i].name, this.elements[i].value);
			break;
		case 'SELECT':
			switch (this.elements[i].type) {
			case 'select-one':
				if(this.elements[i].value)
					data.append(this.elements[i].name, this.elements[i].value);
				break;
			case 'select-multiple':
				for (j = this.elements[i].options.length - 1; j >= 0; j = j - 1) {
					if (this.elements[i].options[j].selected) {
						data.append(this.elements[i].name, this.elements[i].options[j].value);
					}
				}
				break;
			}
			break;
		case 'BUTTON':
			switch (this.elements[i].type) {
			case 'reset':
			case 'submit':
			case 'button':
				data.append(this.elements[i].name, this.elements[i].value);
				break;
			}
			break;
		}
	}
	return data;
}
function serializeJSON(){
	var i, j, q = [];
	var data = {};
	var elements = this.elements;
	if(!this.elements)
		elements = this.find('*');
	for (i = elements.length - 1; i >= 0; i = i - 1) {
		if (elements[i].name === "") {
			continue;
		}
		switch (elements[i].nodeName) {
		case 'INPUT':
			switch (elements[i].type) {
			case 'text':
			case 'hidden':
			case 'password':
			case 'button':
			case 'reset':
			case 'submit':
			case 'number':
			case 'date':
			case 'email':
			case 'tel':
				if(elements[i].name.includes('[]') && elements[i].value){
					name = elements[i].name.replace('[]','');
					if(!data[name])
						data[name] = [];
					data[name].push(elements[i].value);
				}
				else if(elements[i].value)
					data[elements[i].name] = elements[i].value;
				break;
			case 'checkbox':
			case 'radio':
				if (elements[i].checked) {
					data[elements[i].name] = elements[i].value;
				}
				break;
			case 'file':
				if(elements[i].name.includes('[]') && elements[i].value){
					name = elements[i].name.replace('[]','');
					if(!data[name])
						data[name] = [];
					data[name].push(elements[i].value);
				}else{
					if(elements[i].name == 'images'){
						if(!data['images'])
							data['images'] = [];
						data['images'].push(elements[i].get('value'));
					}else{
						data[elements[i].name] = elements[i].get('value');
					}
				}

				break;
			}
			break; 
		case 'TEXTAREA':
			if(elements[i].value)
				data[elements[i].name] = elements[i].value;
			break;
		case 'SELECT':
			switch (elements[i].type) {
			case 'select-one':
				if(elements[i].name.includes('[]') && elements[i].value){
					name = elements[i].name.replace('[]','');
					if(!data[name])
						data[name] = [];
					data[name].push(elements[i].value);
				}
				else if(elements[i].value)
					data[elements[i].name] = elements[i].value;
				break;
			case 'select-multiple':
				for (j = elements[i].options.length - 1; j >= 0; j = j - 1) {
					if (elements[i].options[j].selected) {
						data[elements[i].name] = elements[i].options[j].value;
					}
				}
				break;
			}
			break;
		case 'BUTTON':
			switch (elements[i].type) {
			case 'reset':
			case 'submit':
			case 'button':
				data[elements[i].name] = elements[i].value;
				break;
			}
			break;
		}
	}
	for(key in data){
		try{
			val = JSON.parse(data[key]);
			if(Array.isArray(val))
				data[key] = val;
		}catch(e){

		}
	}
	return data;
}
HTMLFormElement.prototype.serializeJSON = serializeJSON;
HTMLFormElement.prototype.serialize = serialize;
Array.prototype.serialize = function(){
	return this[0].serialize();
};
Array.prototype.serializeJSON = function(){
	return this[0].serializeJSON();
};
Element.prototype.serializeJSON = serializeJSON;
cookie = function(){};
cookie.toString = function(){return document.cookie;};
cookie.get = function (cname) {
	name = cname + "=";
	decodedCookie = decodeURIComponent(cookie);
	ca = decodedCookie.split(';');
	for(i = 0; i <ca.length; i++) {
		c = ca[i];
		while (c.charAt(0) == ' ') {
			c = c.substring(1);
		}
		if (c.indexOf(name) == 0) {
			return c.substring(name.length, c.length);
		}
	}
	return "";
};
storage = localStorage;
history = window.history;

function render(template,block,data){
	var block = $(block);
	block.html(templates[template](data));
}

document.ready = function(listener){
	document.onreadystatechange = function(){
		if(document.readyState == 'complete')
			listener();
	};
};

function getTemplate(node){
	return node.content.cloneNode(true);
}