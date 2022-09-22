
let number = document.getElementById('num')
let percentage = document.getElementById('percentage')
let status_ = document.getElementById('status')
let start = 0
let end = Math.round(percentage.innerHTML)
let counter = 0
let status_val = ''
// status_.style.color('red')
console.log(end)
if (end == 17 || end == 18 ) {
    end = 97
    status_val = 'NORMAL'
}
if (end == 19 || end == 20 ) {
    end = 98
    status_val = 'NORMAL'
}
if (end == 21 || end == 22 ) {
    end = 99
    status_val = 'NORMAL'

}if (end == 23 || end == 24 || end == 25) {
    end = 100
    status_val = 'NORMAL'

}
if (end < 17 ) {
    end = 93 
    status_val = 'UNDER WEIGHT'

}
if (end < 25 && end > 40 ) {
    end = 85
    status_val = 'OVER WEIGHT'

}
if (end > 40 && end < 50) {
    end = 75
    status_val = 'OBESE'

}
function setup() {

  createCanvas(400, 400);
  i = j = k = -90;
  angleMode(DEGREES);
  }

function draw() {
    textSize(20);
    text(end , 100, 100);
    translate(200, 200);
    stroke(255,0,0);
    strokeWeight(10);
    fill(0);
    arc(0, 0, 200, 200, -90, i);
    stroke(255)
    if ( i < ( 360 * end / 100 ) - 90 ) {
        i += 1; 
    }
}


setInterval(() => {
    if(start == end) {
        clearInterval();
    }
    else {
        counter += 1
        start = counter ;
        number.innerHTML = start + '%'
    }
},60);

status_.innerHTML = 'BMI Status' +' '+ status_val





