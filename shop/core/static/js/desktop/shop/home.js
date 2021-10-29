class Home extends Buy{
    constructor(){
        super();
        pageObject.navigation = new Navigation();
    }
}
class Main extends Home{
    constructor(){
        super();
    }
}