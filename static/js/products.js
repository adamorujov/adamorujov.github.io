$(document).ready(function () {
    $("#filterIcon").click(function (e) {
        e.preventDefault()
        $(".myRow").slideToggle()
        $(".myRow").toggleClass("d-flex")
    });


});
window.onload = function () {
    slideOne();
    slideTwo();
}

let sliderOne = document.getElementById("slider-1");
let sliderTwo = document.getElementById("slider-2");
let displayValOne = document.getElementById("range1");
let displayValTwo = document.getElementById("range2");
let displayValOneInput = document.getElementById("rangeInput1");
let displayValTwoInput = document.getElementById("rangeInput2");
let minGap = 0;
let sliderTrack = document.querySelector(".slider-track");
let sliderMaxValue = document.getElementById("slider-1").max;

function slideOne() {
    if (parseInt(sliderTwo.value) - parseInt(sliderOne.value) <= minGap) {
        sliderOne.value = parseInt(sliderTwo.value) - minGap;
    }
    displayValOne.textContent = sliderOne.value;
    displayValOneInput.textContent = sliderOne.value;
    fillColor();
}

function slideTwo() {
    if (parseInt(sliderTwo.value) - parseInt(sliderOne.value) <= minGap) {
        sliderTwo.value = parseInt(sliderOne.value) + minGap;
    }
    displayValTwo.textContent = sliderTwo.value;
    displayValTwoInput.textContent = sliderTwo.value;
    fillColor();
}

function fillColor() {
    percent1 = (sliderOne.value / sliderMaxValue) * 100;
    percent2 = (sliderTwo.value / sliderMaxValue) * 100;
    sliderTrack.style.background = `linear-gradient(to right, rgb(218, 218, 229) ${percent1}% , rgb(203, 3, 29) ${percent1}% , rgb(203, 3, 29) ${percent2}%, rgb(218, 218, 229) ${percent2}%)`;
}