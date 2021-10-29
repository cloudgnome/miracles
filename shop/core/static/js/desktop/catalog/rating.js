class Rating{
    constructor(){
        this.value = parseInt($('#rating').value);
        this.stars = $('#ratingStars i');

        this.fill(this.value);

        this.stars.on('mouseover',this.hover.bind(this));
        this.stars.on('mouseout',this.out.bind(this));
        this.stars.on('click',this.click.bind(this));
    }
    click(event){
        var target = event.target;
        var number = target.get('number');
        this.value = number;

        event.stopPropagation();
        event.preventDefault();
        return false;
    }
    hover(event){
        var target = event.target;
        this.empty();
        this.fill(this.stars.indexOf(target) + 1);

        event.stopPropagation();
        event.preventDefault();

        return false;
    }
    out(event){
        this.empty();
        this.fill(this.value);

        event.stopPropagation();
        event.preventDefault();

        return false;
    }
    fill(value){
        var i = 0;
        while(i < value){
            this.stars[i].renameClass('far','fa');
            i++;
        }
    }
    empty(){
        this.stars.each(function(elem){
            elem.renameClass('fa','far');
        });
    }
}