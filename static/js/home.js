const images = [
    "/static/images/bg1.jpeg",
    "/static/images/bg2.jpeg",
    "/static/images/bg3.jpeg"
];

const quotes = [
    "Poor dietary habits are major contributors to chronic diseases.",
    "Small food choices today decide your long-term health.",
    "Understand your nutrition before disease understands you.",
    "Data-driven diet decisions can prevent lifestyle disorders."
];

let index = 0;

function changeBackgroundAndQuote() {
    const bgEl = document.getElementById("bg");
    const quoteEl = document.getElementById("quote");

    if (bgEl) {
        bgEl.style.backgroundImage = `url(${images[index]})`;
    }

    if (quoteEl) {
        quoteEl.innerText = quotes[index];
    }

    index = (index + 1) % images.length;
}

changeBackgroundAndQuote();
setInterval(changeBackgroundAndQuote, 15000);
