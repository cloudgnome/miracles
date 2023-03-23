class Http extends XMLHttpRequest{
	static CSRF_METHODS = ['POST','PUT','DELETE'];

	constructor(href,context = {title:document.title}){
		super();

		this.context = context;
		this.title = context.title;
		this.href = href;
	}
	static click(e){
		var href = e.target.get('href');

		if(!href){
			if(e.target.tagName != 'A'){
				e.target.closer('a').click();
			}
			e.stopPropagation();
			e.preventDefault();
			return;
		}

		let context = Http.parse_url(href);

		if(!context || !Object.keys(context).length)
			return;

		e.stopPropagation();
		e.preventDefault();

		context.title = e.target.get('title') ? e.target.get('title') : e.target.text;

		GET(href,context);

		return false;
	}
	process_template(View,html){
		if(View.block){
			$(View.block).html(html);
			$(`${View.block} a`).on('click',Http.click.bind(this));

			try{
				$(`${View.block} script`).each((elem) => {
					eval(elem.text);
				});
			}catch(e){
				log(e);
			}
		}
	}
	process_request(){
		Http.requests.push(this.href);
		Http.loading.show();

		this.setRequestHeader('X-Requested-With','XMLHttpRequest');
		this.onreadystatechange = () =>{
			switch(this.readyState){
				case 4:
					Http.requests.pop(this.href);
					this.process_response();
					break;
			}
		};
		this.send(this.context.data ? this.context.data : undefined);
	}
	process_response(){
		if(this.status != 200){
			this.alert(this.status);
		}

		if(this.getResponseHeader('Content-Type') == 'application/json'){
			try{
				this.json = JSON.parse(this.responseText);
				this.errors = this.json.errors;
			}catch(e){
				log(e);
			}
		}else{
			this.html = this.responseText;
		}

		if(!Http.requests.length)
			Http.loading.hide();

		this.View = Http.process_view(this);
		Http.lastView = this.View;

		if(this.View && this.context && !this.context.history && this.context.defaultView)
			Http.history.pushState(this);
	}
	static process_view(response = {}){
		let View;


		if(response && response.context && response.context.View)
			View = response.context.View;
		else{
			if(!response.href){
				response.href = location.pathname + location.search + location.hash;
			}

			if(!response.context){
				response.context = Http.parse_url(response.href,response.method);
			}

			if(!response.View){
				try{
					View = eval(response.context.Model + response.context.defaultView.name);
				}catch(e){
					log(e);
					View = response.context.defaultView;
				}
			}else{
				View = response.View;
			}

		}

		if(response.html)
			response.process_template(View,response.html);

		if(window.PAGE_CONTEXT && Object.keys(window.PAGE_CONTEXT).length)
			Object.assign(response,window.PAGE_CONTEXT);

		Http.lastResponse = response;

		try{
			return new View(response);
		}catch(e){
			log(e);
			log(View);
			if(View)
				return View(response);
		}
	}
	create_href(){
		if(this.href[0] == '?'){
			this.method = 'POST';
		}

		if(this.context && this.context.href)
			this.href = this.context.href;

		this.url = new URL(this.href,location.origin);

		try{
			this.View = eval(this.context.Model + this.context.defaultView.name);
		}catch(e){
			/*log(e);*/
			this.View = this.context.defaultView;
		}

		if(this.href.match("/(?<Model>[A-Z][a-z]+)($|\\?[\\s\\S])") && !['PUT','DELETE'].includes(this.method))
			this.url.searchParams.set('limit',this.View.limit ? this.View.limit : 10);

		this.href = this.url.href;
	}
	static parse_url(href,method = 'GET'){
		if(!href){
			href = location.pathname + location.search + location.hash;
		}

		if(href[0] == '?'){
			method = 'POST';
			let oparams = new URLSearchParams(location.search);
			let params = new URLSearchParams(href);

			for(let [k,v] of params.entries()){
				oparams.set(k,v);
			}

			href = `${location.pathname}?${oparams}`;
		}

		for(let [pattern,defaultViews] of Object.entries(urlpatterns)){
			let regex = new RegExp(pattern);

			if(regex.test(href)){
				regex = regex.exec(href);

				if(regex.groups){
					regex.groups.href = href;
					regex.groups.defaultView = defaultViews[method];
					return regex.groups;
				}else{
					return {defaultView:defaultViews[method],View:defaultViews[method],href:href};
				}

				break;
			}
		}
	}
	renderErrors(){
		text = '';
		errors = this.json.errors;
		for(error in errors){
			text += `${error}: ${JSON.stringify(errors[error])}` + '<br> <br>';
		}
		this.alert(text,10000);
	}
	alert(text,scnds){
		Http.alert(text,scnds);
	}
	static alert(text,scnds){

		Http.alert_message.text(text);
		Http.alert_container.show();

		if(!scnds)
			scnds = 3000;

		timeout = setTimeout(() => {
			Http.alert_container.hide()
		},scnds);

		Http.alert_container.on('mouseover',() => {
			if(timeout)
				clearTimeout(timeout);
		});
		Http.alert_container.on('mouseout',() => {
			timeout = setTimeout(() => {
				Http.alert_container.hide()
			},3000);
		});
	}
}
Http.requests = [];
Http.history = new History();

$('body').append(render($('#http-loading-template')));
$('body').append(render($('#http-alert-template')));

Http.loading = $('#http-loading');
Http.alert_container = $('#http-alert');
Http.alert_message = $('#http-alert-message');

$('#http-alert .close').on('click',function(){
	Http.alert_container.hide();
});

if(!Http.url)
	Http.url = new URL(location.origin + location.pathname + location.search);

class HttpMethod extends Http{
	constructor(method,href,context = {}){
		super(href,context);
		this.method = method;

		Object.assign(this.context,Http.parse_url(href,method));

		this.create_href();
		this.open(this.method,this.href);

		if(Http.CSRF_METHODS.includes(this.method)){
			this.setRequestHeader("X-CSRFToken", cookie.get('csrftoken'));

			if(typeof this.context.data == 'object'){
				this.context.data.csrf_token = cookie.get('csrftoken');
				this.context.data = JSON.stringify(this.context.data);
				this.setRequestHeader("Content-Type", "application/json");
			}
			else{
				this.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
			}
		}

		this.process_request();
	}
}

function GET(href,context){
	return new HttpMethod(method="GET",href,context);
}

function POST(href,context){
	return new HttpMethod(method="POST",href,context);
}

function PUT(href,context){
	return new HttpMethod(method="PUT",href,context);
}

function DELETE(href,context){
	return new HttpMethod(method="DELETE",href,context);
}

function OPTIONS(href,context){
	return new HttpMethod(method="OPTIONS",href,context);
}