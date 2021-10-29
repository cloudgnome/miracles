class Navigation{
    constructor(container){
        this.container = container;

        this.touchStartPositionX;
        this.touchStartPositionY;
        this.touchEndPositionX = 0;
        this.touchEndPositionY = 0;
        this.verbose = false;
        this.active = false;
        this.backButton = container.find('.back')[0];
        this.catConainer = container.find('.navCategories')[0];
        this.loading = container.find('.loading');

        $('#menu').on('scroll',this.resizeBackButton.bind(this));

        container.find('.click').on('click',this.sub.bind(this));

        this.catConainer.on('touchstart',this.touchStart.bind(this));
        this.catConainer.on('touchend',this.touchEnd.bind(this));

        this.backButton.on('click touch',this.back.bind(this));
    }
    resizeBackButton(e){
        var top = ((window.screen.height - 264) - $('#menu .navigation')[0].offsetTop) + $('#menu').scrollTop;

        if(top > this.catConainer.height() / 2)
            top = this.catConainer.height() / 2;

        this.backButton.find('i')[0].css('top',`${top}px`);
    }
    touchStart(e){
        if(e.changedTouches){
            this.touchStartPositionX = e.changedTouches[0].clientX;
            this.touchStartPositionY = e.changedTouches[0].clientY;
        }
        else{
            this.touchStartPositionX = e.clientX;
            this.touchStartPositionY = e.clientY;
        }

        if(this.verbose){
            log('touchStartPositionX is: ' + this.touchStartPositionX);
            log('touchStartPositionY is: ' + this.touchStartPositionY);
        }
    }
    touchEnd(e){
        this.touchEndPositionX = e.changedTouches[0].clientX;
        this.touchEndPositionY = e.changedTouches[0].clientY;

        if(this.verbose){
            log('touchEndPositionX is: ' + this.touchEndPositionX);
            log('touchEndPositionY is: ' + this.touchEndPositionY);
        }

        var diffX = this.touchEndPositionX - this.touchStartPositionX;
        var diffY = this.touchEndPositionY - this.touchStartPositionY;

        if(this.touchEndPositionX != this.touchStartPositionX && diffX > 100 && diffY < 50){
            this.back();
        }
    }
    back(){
        var last = this.container.find('.sub.active').last();
        last.removeClass('active');
        last.prev().removeClass('active');

        if(!this.container.find('.sub.active').length)
            this.backButton.removeClass('active');

        this.changeHeight();
    }
    changeHeight(){
        var last = this.container.find('.sub.active').last();
        if(!last){
            this.catConainer.removeAttr('style');
            return;
        }
        var h = last.height();
        this.catConainer.css('height',h + 'px');
    }
    sub(e){
        if(e.target.hasClass('image')){
            e.target.parent().click();
            e.stopPropagation();
            e.preventDefault();
            return false;
        }

        if(e.target.find('.sub').length && e.target.find('.sub')[0].hasClass('active'))
            return false;

        var sub = e.target.find('.sub');

        if(sub.length){
            this.container.find('.nav-bg.active').removeClass('active');
            setTimeout(function(){
                e.target.find('.nav-bg')[0].active();
            },300);
        }

        if(sub.length){
            sub[0].active();
            this.backButton.addClass('active');
        }
        else{
            var a = e.target.find('a');
            if(a.length)
                a[0].click();
        }
        if(sub.length){
            this.changeHeight();
            this.resizeBackButton();
        }
    }
}