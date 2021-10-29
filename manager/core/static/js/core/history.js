class History{
    constructor(){
        window.onpopstate = this.popState.bind(this);
        this.history = window.history;
    }
    pushState(request){
        if(['PUT','DELETE'].includes(request.method))
            return;

        var state = {
            'href'   :request.href,
            'Model'  :request.context.Model,
            'View'   :request.View ? request.View.__proto__.constructor.name : undefined,
            'defaultView':request.context.defaultView.__proto__.constructor.name,
            'title'  :request.title,
            'data'   :request.context.data ? request.context.data : undefined,
            'method' :request.method,
        };

        this.history.pushState(state,request.title,request.href);
    }
    popState(e){
        let state = e.state;

        if(location.hash)
            return;

        if(!state){
            state = Http.find_view();

            state.href = state.href.replace(location.hash,'');
        }

        let url = new URL(state.href,location.origin);
        let href = url.pathname + url.search;

        GET(href,{history:true});
    }
}