class Buy{
    constructor(){
        this.timeout = NaN;
        this.cartButton = $('#cart-button');
        this.toTarget = $('#cart-button');

        $('.buy').on('click touch',this.buy.bind(this));

        $('.quantity .minus').on('click touch',this.minus.bind(this));
        $('.quantity .plus').on('click touch',this.plus.bind(this));
        $('.quantity input').on('change',this.input.bind(this));
    }
    input(event){
        var target = event.target;
        var qty = target.value;

        if(qty < 1 || isNaN(qty)){
            qty = 1;
            target.value = 1;
        }
    }
    minus(event){
        var target = event.target;
        var input = target.next();
        var qty = input.value * 1 - 1;

        if(qty > 0){
            input.value = qty;
        }
        return false;
    }
    plus(event){
        var target = event.target;
        var input = target.prev();
        var qty = input.value * 1 + 1;

        if(qty > 1){
            input.value = qty;
        }
    }
    buy(event){
        var target = event.target;
        var parent = target.parent();
        var qty = target.closer('input[name="quantity"]');
        var id = target.get('value');

        if(!storage.qty || storage.qty == 'NaN')
            storage.qty = Object.keys(cart).length;

        if(!qty){
            var qty = 1;
        }else{
            var qty = qty.value ? qty.value : 1;
        }

        if(!pageObject.cart[id]){
            pageObject.cart[id] = qty;
            storage.qty++; 
            pageObject.cartQty.text(storage.qty);
        }
        else{
            pageObject.cart[id] = parseInt(pageObject.cart[id]) + qty * 1;
        }

        pageObject.message(`${target.closer('.name').text()} ${qty}шт.`);

        storage.cart = JSON.stringify(pageObject.cart);

        this.animate(this.getDataToAnimate(target));
    }
    getDataToAnimate(target){
        var img = target.closer('img');
        var item = target.parent().getBoundingClientRect();
        var toTarget = this.toTarget;

        return [img,item,toTarget]
    }
    animate(data){
        var that = this;

        var img = data[0];
        var item = data[1];
        var toTarget = data[2];
        var toTargetData = toTarget.getBoundingClientRect();

        var i = create('img');
        i.set('src',img.src);
        i.css('left',`${item['x']}px`);
        i.css('top',`${item['y']}px`);
        i.css('z-index','9999');
        i.set('class','animateBuy');
        body[0].append(i);

        setTimeout(function(){
            i.css('left',`${toTargetData['x']}px`);
            i.css('top',`${toTargetData['y']}px`);
            i.css('height',`20px`);
            i.css('width',`20px`);
            setTimeout(function(){
                i.remove();
                toTarget.active();
                setTimeout(function(){
                    toTarget.active();
                },300);
            },700);
        },300);
    }
}