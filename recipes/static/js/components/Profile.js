class Profile extends MainCards{
    constructor(container, card, counter, api, userAuth,button) {
        super(container, card, counter, api, userAuth,button);
        this.tooltipAdd = this.tooltipAdd.bind(this);
        this.tooltipDel = this.tooltipDel.bind(this)
    }
    
    _eventSubscribe  (target)  {
        const cardId = target.closest(this.card).getAttribute('second-id');
        if(target.hasAttribute('data-out')) {
            this.button.subscribe.addSubscribe(target,cardId)
        } else {
            this.button.subscribe.removeSubscribe(target,cardId)
        }
    }
}