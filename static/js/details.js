$(document).ready(function () {
    $("#writeComment").click(function (e) {
        e.preventDefault();
        $(".writeCommentRow").slideToggle();
    })

    let tabNames = document.querySelectorAll(".tabName")
    tabNames.forEach(tName => {
        tName.onclick = function () {
            let dataId = tName.getAttribute("data-id")

            tabNames.forEach(tn => {
                tn.classList.remove("tabActive")
            })
            let tab = document.getElementById(dataId)
            let tabs = document.querySelectorAll(".tab")
            tabs.forEach(t => {
                t.classList.add("d-none")
            })
            tName.classList.add("tabActive")
            tab.classList.remove("d-none")
        }
    })
    $(".sizeLi").click(function () {

        if (!$(this).hasClass("isSelectedSize")) {
            $(this).toggleClass("isSelectedSize");
        }    
        $(this).siblings().removeClass("isSelectedSize")
        let sizeValue = $(this).attr("data-value")
        $(".sizeVal").children().first().html(sizeValue)

    })
    $('.related').owlCarousel({
        loop: true,
        margin: 10,
        nav: false,
        dots: false,
        responsive: {
            0: {
                items: 1
            },
            550: {
                items: 2
            },
            820: {
                items: 3
            },
            1200: {
                items: 4
            }
        }
    })
    if ($(".related .owl-item").hasClass("active")) {
        $(".related .owl-item").siblings().addClass("d-flex justify-content-center")
    }
    $('.recently').owlCarousel({
        loop: true,
        margin: 10,
        nav: false,
        dots: false,
        responsive: {
            0: {
                items: 1
            },
            550: {
                items: 2
            },
            820: {
                items: 3
            },
            1200: {
                items: 4
            }
        }
    })
    if ($(".recently .owl-item").hasClass("active")) {
        $(".recently .owl-item").siblings().addClass("d-flex justify-content-center")
    }
    $(".whishListIcon").click(function (e) {
        e.preventDefault()
        $(this).toggleClass("bi-heart-fill whishListBackground")
        $(this).toggleClass("bi-heart")

    })
    let plMinus = document.querySelector(".minus")
    let plPlus = document.querySelector(".plus")
    let plproductCount = document.querySelector("#productCounter")
    plPlus.addEventListener("click", () => {
        plproductCount.value = Number(plproductCount.value) + 1;
    })
    plMinus.addEventListener("click", () => {
        if (plproductCount.value > 0) {
            plproductCount.value = Number(plproductCount.value) - 1;
        } else {
            alert("Number of the products can't be lower than zero")
        }
    })

    $(".smallImages .image img").click(function () {
        let smImageAttr = $(this).attr("src")
        let bigImageAttr = $(".detailsRowBigImage .bigImage img").attr("src", smImageAttr)
        $(this).parent().toggleClass("opacity-100")
        $(this).parent().siblings().css("transition", "0.3s").removeClass("opacity-100")
        console.log(bigImageAttr);
    })

    $(".colorLi").click(function (e) {
        e.preventDefault()
        if (!$(this).hasClass("isSelectedColor")) {
            $(this).toggleClass("isSelectedColor");
        }

        $(this).siblings().removeClass("isSelectedColor")
        let colorValue = $(this).attr("data-value")
        $(".colorVal").children().first().html(colorValue)
    })

    // $(".bigImage img").imagezoomsl({
    //     zoomrange: [3, 3]
    // })
})