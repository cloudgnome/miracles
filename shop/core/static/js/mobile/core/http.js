http = new XMLHttpRequest();
body = $('body');
loading = create('div');
loading.hide();
loading.set('id','loading');
bg = create('div');
bg.hide();
bg.set('id','bg');
body.append(bg);
body.append(loading);
http.loading = loading;
http.bg = bg;

http.progress = false;
http.get = function (url) {
	this.method = 'GET';
	this.url = url;
	this.request();
};
http.post = function (url, data) {
	this.method = 'POST';
	this.url = url;
	this.data = data;
	this.request();
};
http.response = http.responseText;
http.onreadystatechange = function () {
	switch (this.readyState) {
		case 4:
			this.loading.hide();
			this.progress = false;
			if (this.status == 200) {
				if (this.getResponseHeader('Content-Type') == 'application/json') {
					try {
						this.json = JSON.parse(this.responseText);
					} catch (e) {
						console.log(e);
					}
				}
				this.text = this.responseText;
				try {
					this.action();
				} catch (e) {
					log(e);
					/*this.render();*/
				}
			}
			else {
				this.alert(this.status);
			}
			break;
	}
};
http.request = function () {
	if (this.progress)
		return;
	this.loading.show();
	this.open(this.method, this.url);
	if (this.method == 'POST') {
		if (this.data instanceof FormData) {
			this.setRequestHeader("X-CSRFToken", cookie.get('csrftoken'));
		}
		else if (typeof this.data == 'object') {
			this.data = JSON.stringify(this.data);
			this.setRequestHeader("X-CSRFToken", cookie.get('csrftoken'));
			this.setRequestHeader("Content-Type", "application/json");
		}
		else {
			this.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
		}
	}
	this.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
	this.progress = true;
	this.send(this.data);
};

httpAlert = create('div');
httpAlert.set('id', 'http-alert');
message = create('div');
message.set('id', 'message');
close = create('div');
close.set('class', 'close');
httpAlert.append(close);
httpAlert.append(message);
body.append(httpAlert);
timeout = false;
http.alert = function (text, scnds) {
	if (!scnds)
		scnds = 3000;
	message.html(text);
	httpAlert.active();
	timeout = setTimeout(function () { httpAlert.active() }, scnds);
};
httpAlert.on('mouseover', function () {
	if (timeout)
		clearTimeout(timeout);
});
httpAlert.on('mouseout', function () {
	timeout = setTimeout(function () { httpAlert.hide() }, 3000);
});
close.on('click', function () {
	httpAlert.hide();
});
http.renderErrors = function () {
	text = '';
	errors = this.json.errors;
	for (error in errors) {
		text += `${error}: ${errors[error]}` + '<br> <br>';
	}
	this.alert(text, 10000)
};