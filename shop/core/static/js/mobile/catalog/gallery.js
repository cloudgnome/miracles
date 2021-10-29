class Gallery{
    constructor(gallery){
        this.gallery = gallery;

        $('#bg').on('click',this.close.bind(this));
        $('#big-photo, .gallery a').on('click',this.open.bind(this));
    }
    open(event){
        this.current = event.target.get('data-image');
        this.counter = this.gallery.indexOf(this.current);
        var template = getTemplate($('#galleryTemplate'));

        $('body').append(template);
        this.container = $('#gallery');
        this.containerImage = $('#gallery img');

        this.container.find('.close').on('click',this.close.bind(this));

        for(var src of gallery){
            var img = create('img');
            img.src = src;
            this.container.append(img);
        }

        $('#bg').show();
        setTimeout(function(){
            $('#gallery .close').addClass('show');
            $('#gallery').addClass('show');
        },200);

        event.preventDefault();
        event.stopPropagation();
        return false;
    }
    close(){
        if(this.container){
            this.container.remove();
            $('#bg').hide();
        }
    }
}