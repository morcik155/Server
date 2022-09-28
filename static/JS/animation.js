let start = Date.now();

let timer = setInterval(function () {
    let timePassed = Date.now() - start;
    hello_text.style.opacity = timePassed / 2000;


    if (timePassed > 2000) clearInterval(timer);

}, 20);
