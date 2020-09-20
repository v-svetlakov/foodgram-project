class Header {
    constructor(counter) {
        this.counter = counter;
        this.api = api;
        this.counterNum = this.counter.textContent;
        this.plusCounter = this.plusCounter.bind(this);
        this.minusCounter = this.minusCounter.bind(this);
        this.changeCounterColor = this.changeCounterColor.bind(this);
    }

    plusCounter  ()  {
        this.counterNum = ++this.counterNum;
        this.counter.textContent = this.counterNum;
    }
    minusCounter ()  {
        this.counterNum = --this.counterNum;
        this.counter.textContent = this.counterNum;
        this.changeCounterColor();
    }
    changeCounterColor() {
        if (this.counterNum === 0) {
          this.counter.classList.remove('badge_style_blue');
           
      this.counter.classList.add('badge_style_zero');
        }
      }
}
