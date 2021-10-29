class Select{
    constructor(parameters){
        var container = parameters.container;
        this.select = container.find('select')[0];
        this.id = this.select.id;

        var template = getTemplate($('#selectTemplate'));
        this.selectOptions = template.querySelector('.select-items');
        this.textContainer = template.querySelector('.select-selected');

        this.container = container;
        this.parameters = parameters;

        this.createOptions();

        if(!this.selected){
            this.select.selectedIndex = 0;
            this.selected = this.select.options[0];
        }

        this.head();

        this.select.dispatchEvent(new Event('change'));
        Select.selects[this.id] = this;
    }
    disable(index){
        this.select.options[index].disabled = true;
        this.options[index].addClass('disabled');
    }
    enable(index){
        this.select.options[index].disabled = false;
        this.options[index].removeClass('disabled');
    }
    pick(index){
        this.selected.removeClass('selected');

        this.select.selectedIndex = index;
        this.select.dispatchEvent(new Event('change'));

        this.options[index].addClass('selected');

        this.textContainer.innerHTML = this.options[index].innerHTML;
    }
    reload(){
        for(var option of this.options){
            option.removeClass('selected');
            option.removeClass('disabled');
        }

        this.select.selectedIndex = this.options[0].index;
        this.textContainer.innerHTML = this.options[0].innerHTML;
        this.options[0].addClass('selected');
    }
    head(){
        var selectedText = this.selected.innerHTML;

        this.textContainer.innerHTML = selectedText;
        this.textContainer.addEventListener('click',this.toggle.bind(this));
    }
    createOptions(){
        for (var option of this.select.options){

            var optionTemplate = create('div');
            optionTemplate.set('value',option.index);
            optionTemplate.innerHTML = option.innerHTML;

            if(option.selected){
                optionTemplate.addClass('selected');
                this.select.selectedIndex = option.index;
            }

            this.selectOptions.append(optionTemplate);
        }
        this.container.append(this.textContainer);
        this.container.append(this.selectOptions);

        this.options = this.container.find('.select-items div');
        this.options.on('click',this.change.bind(this));
    }
    change(e){
        var target = e.target;

        if(target.hasClass('disabled'))
            return;

        this.pick(this.select.options[target.get('value')].index);
        this.closeAll();

        if(this.parameters && this.parameters.handler)
            this.parameters.handler();
    }
    toggle(e){
        var target = e.target;

        this.closeAll(target);

        this.container.active();

        e.stopPropagation();
    }
    closeAll(target) {
        for(var [selector,select] of Object.entries(Select.selects)){
            if(select.textContainer != target)
                select.container.removeClass('active');
        }
    }
}
Select.selects = {};

function customizeSelect(parameters){
    if(parameters && parameters.items)
        var containers = parameters.items;
    else{
        var containers = $('.custom-select');
    }

    var result = {};
    for(var container of containers){
        var select = new Select({container:container});
        result[select.id] = select;
    }

    return result;
}