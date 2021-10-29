class Home extends Buy{
    constructor(){
        super();
        this.sliderLength = $('#slider a').length;
        this.index = 0;
        this.touchStartPosition;
        this.sliderTimeout;
        this.verbose = false;
        this.container = $('#slider');
        this.image = $('#slider a')[0];
        this.touchEndPosition = 0;

        if($('#slider a').length > 1){
            this.sliderInverval = setInterval(this.slide.bind(this),3000);

            this.container.on("touchstart",this.start.bind(this));
            this.container.on("touchend",this.stop.bind(this));
        }

        new Navigation($('main .navigation')[0]);
    }
    start(e){
        if(this.sliderInverval)
            clearInterval(this.sliderInverval);

        if(e.changedTouches)
            this.touchStartPosition = e.changedTouches[0].clientX;
        else{
            this.touchStartPosition = e.clientX;
        }

        if(this.verbose)
            log('touchStartPosition is: ' + this.touchStartPosition);
    }
    stop(e){
        if(this.sliderInverval)
            clearInterval(this.sliderInverval);

        if(this.sliderTimeout)
            clearTimeout(this.sliderTimeout);

        this.touchEndPosition = e.changedTouches[0].clientX;

        if(this.verbose)
            log('touchEndPosition is: ' + this.touchEndPosition);

        if(this.touchEndPosition < this.touchStartPosition)
            this.index++;
        else if(this.touchEndPosition > this.touchStartPosition)
            this.index--;

        this.slide(true);

        var that = this;
        this.sliderTimeout = setTimeout(function(){
            that.sliderInverval = setInterval(that.slide.bind(that),2000);
        },2000);

        e.preventDefault();
        e.stopPropagation();
        return false;
    }
    slide(touch){
        if(!touch && this.sliderInverval)
            this.index++;

        if(this.index >= this.sliderLength){
            if(!touch && this.sliderInverval)
                this.index = 0;
            else if(touch && !this.sliderInverval){
                this.index = this.sliderLength;
                return;
            }
        }

        if(this.index < 0){
            this.index = 0;
            return;
        }

        if(this.verbose)
            log('index is: ' + this.index);

        this.image.css('margin-left',this.index * -100 + '%');
    }
}
class Main extends Home{
    constructor(){
        super();
    }
}