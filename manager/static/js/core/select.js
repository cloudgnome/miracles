class Select{
    constructor(parameters){
        var container = parameters.container;
        this.select = container.find('select')[0];

        if(!this.select.options.length)
            return;

        this.id = this.select.id;
        this.select.indexOf = {};

        var template = render($('#selectTemplate'));
        this.selectOptions = template.querySelector('.select-items');
        this.textContainer = template.querySelector('.select-selected');
        this.wrapper = this.selectOptions.querySelector('.sel-items-wrapper');

        this.container = container;
        this.parameters = parameters;

        this.createOptions();

        this.head();

        this.select.dispatchEvent(new Event('change'));
        Select.selects[this.id] = this;
    }
    createOptions(){
        for (var option of this.select.options){

            var optionTemplate = create('div');
            optionTemplate.set('value',option.value);
            this.select.indexOf[option.value] = option.index;
            optionTemplate.innerHTML = option.innerHTML;

            if(option.selected){
                optionTemplate.addClass('selected');
                this.select.selectedIndex = option.index;
                this.selected = option.value;
            }

            this.wrapper.append(optionTemplate);
        }
        this.container.append(this.textContainer);
        this.container.append(this.selectOptions);

        this.options = {};
        for(var option of this.container.find('.select-items div')){
            this.options[option.get('value')] = option;
            option.on('click',this.change.bind(this));
        }
    }
    change(e){
        log(e);
        if(!e.isTrusted)
            return;

        let target = e.target;
        let value = target.get('value');

        if(target.hasClass('disabled'))
            return;

        this.pick(value);
        this.closeAll();

        if(this.parameters && this.parameters.handler)
            this.parameters.handler();

        e.stopPropagation();
        return false;
    }
    disable(index){
        this.select.options[index].disabled = true;
        this.options[index].addClass('disabled');
    }
    enable(index){
        this.select.options[index].disabled = false;
        this.options[index].removeClass('disabled');
    }
    pick(value){
        if(this.select.indexOf[value] == this.select.selectedIndex)
            return;

        try{
            this.options[this.selected].removeClass('selected');
        }catch(e){
            log(e);
        }

        this.select.selectedIndex = this.select.indexOf[value];
        let e = new Event('change');
        e.trusted = true;
        this.select.dispatchEvent(e);

        this.options[value].addClass('selected');

        this.textContainer.innerHTML = this.options[value].innerHTML;
        this.selected = value;
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
        if(!this.selected)
            var selectedText = this.select.options[0].innerHTML;
        else{
            var selectedText = this.options[this.selected].innerHTML;
        }

        this.textContainer.innerHTML = selectedText;
        this.textContainer.addEventListener('click',this.toggle.bind(this));
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