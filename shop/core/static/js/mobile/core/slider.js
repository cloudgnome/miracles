class Slider{
    constructor(){
        this.container = $('#slider');
        this.galleryItems = $('#slider a');
        this.activeGalleryImage = this.galleryItems[0];
        this.bullets = $('#slider .bullets div');
        this.countBullets = this.bullets.length;
        this.currentBullet = $('#slider .bullets div.active')[0];
        this.bullets.on('click',this.bullet.bind(this));
    }
    prev(){
        var prev = this.activeGalleryImage.prev();
        if(!prev)
            prev = this.galleryItems[this.galleryItems.length - 1];

        prev.hide();
        prev.addClass('left');
        var that = this;
        setTimeout(function(){
            prev.show('flex');
            prev.addClass('active');
            setTimeout(function(){
                that.activeGalleryImage.removeClass('active');
                prev.removeClass('left');
                that.activeGalleryImage = prev;
            },100);
        },100);
        this.bullet(true);
    }
    next(){
        var next = this.activeGalleryImage.next();
        if(!next)
            next = this.galleryItems[0];

        this.activeGalleryImage.addClass('left');
        next.addClass('active');
        var that = this;
        setTimeout(function(){
            that.activeGalleryImage.hide();
            setTimeout(function(){
                that.activeGalleryImage.removeClass('active');
                that.activeGalleryImage.removeClass('left');
                that.activeGalleryImage.show('flex');
                that.activeGalleryImage = next;
            },100);
        },100);
        this.bullet();
    }
    bullet(prev){
        if(prev){
            if(this.bullets.indexOf(this.currentBullet) == 0){
                var currentBullet = this.bullets[this.countBullets - 1];
            }else{
                var currentBullet = this.currentBullet.prev();
            }
        }else{
            if(this.bullets.indexOf(this.currentBullet) == this.countBullets - 1){
                var currentBullet = this.bullets[0];
            }else{
                var currentBullet = this.currentBullet.next();
            }
        }
        this.currentBullet.removeClass('active');
        this.currentBullet = currentBullet;
        this.currentBullet.addClass('active');
    }
}