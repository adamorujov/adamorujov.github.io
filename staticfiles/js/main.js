$(document).ready(function () {
    $("#topFooter .links .linkUl .footerBrands .responsiveBrand").click(function () {
        $("#topFooter .links .linkUl .footerBrands ul").slideToggle()
    })
    $("#topFooter .links .linkUl .footerProducts .responsiveProducts").click(function () {
        $("#topFooter .links .linkUl .footerProducts ul").slideToggle()
    })
    $("#topFooter .links .linkUl .footerInformaton .responsiveInformation").click(function () {
        $("#topFooter .links .linkUl .footerInformaton ul").slideToggle()
    })
    $("#topFooter .getInTouch").click(function () {
        $("#topFooter .info").slideToggle()
    })
    $(".menuIcon").click(function () {
        $(".menu").css("display", "block")
        $(".menu").addClass("animate__slideInLeft")
        $(".menu").removeClass("animate__slideOutLeft")
        $(".searchArea").addClass("animate__slideOutRight")
        $(".searchArea").removeClass("animate__slideInRight")
        $(".basketArea").addClass("animate__slideOutRight")
        $(".basketArea").removeClass("animate__slideInRight")
    })
    $(".closeIcon i").click(function () {
        $(".menu").addClass("animate__slideOutLeft")
        $(".menu").removeClass("animate__slideInLeft")
    })
    $(".menuShopLi").click(function (e) {
        e.preventDefault()
        $(".menuShopUl").slideToggle()
    })
    $(".menuProductsLi").click(function (e) {
        e.preventDefault()
        $(".menuProductsUl").slideToggle()
    })

    $(".userIconLi").click(function () {
        $(".userIconMenuLoginStatusUl").slideToggle()
    })
    $(window).scroll(function () {
        if (window.scrollY >= 650) {
            $(".goUp").removeClass("d-none")
        }
        if (window.scrollY <= 650) {
            $(".goUp").addClass("d-none")
        }
    })
    $(".goUp").click(function () {
        $(window).scrollTop(0);
    })

    $(".addToCard .increase-number-decrease .plus").click(function (e) {
        e.preventDefault()
        $(this).siblings()[1].innerText++;

    })
    $(".addToCard .increase-number-decrease .minus").click(function (e) {
        e.preventDefault()
        if ($(this).siblings()[0].innerText > 1) {
            $(this).siblings()[0].innerText--;
        } else {
            alert("Number of the products can't be lower than 1")
        }
    })
    $(".productsLi a").click(function (e) {
        e.preventDefault()
    })
    $(".shopLi a").click(function (e) {
        e.preventDefault()
    })

    $(".searchIcon").click(function (e) {
        e.preventDefault()
        $(".searchArea").css("display", "block")
        $(".searchArea").addClass("animate__slideInRight")
        $(".searchArea").removeClass("animate__slideOutRight")
        $(".menu").addClass("animate__slideOutLeft")
        $(".menu").removeClass("animate__slideInLeft")
    })
    $(".searchCloseIcon i").click(function () {
        $(".searchArea").addClass("animate__slideOutRight")
        $(".searchArea").removeClass("animate__slideInRight")

    })
    $("section").click(function () {
        $(".searchArea").addClass("animate__slideOutRight")
        $(".searchArea").removeClass("animate__slideInRight")
        $(".menu").addClass("animate__slideOutLeft")
        $(".menu").removeClass("animate__slideInLeft")
        $(".basketArea").addClass("animate__slideOutRight")
        $(".basketArea").removeClass("animate__slideInRight")
    })

    $(".basket").click(function (e) {
        e.preventDefault()
        $(".basketArea").css("display", "block")
        $(".basketArea").addClass("animate__slideInRight")
        $(".basketArea").removeClass("animate__slideOutRight")
        $(".basketTxt-closeIcon").css("display", "flex")
        $(".basketTxt-closeIcon").addClass("animate__slideInRight")
        $(".basketTxt-closeIcon").removeClass("animate__slideOutRight")


        $(".menu").addClass("animate__slideOutLeft")
        $(".menu").removeClass("animate__slideInLeft")
    })
    $(".basketCloseIcon i").click(function (e) {
        e.preventDefault()
        $(".basketArea").addClass("animate__slideOutRight")
        $(".basketArea").removeClass("animate__slideInRight")
    })

    // $(".generalNavBar").hide()
    $(window).scroll(function () {
        if (window.scrollY >= 80) {
            $(".generalNavBar").show()
            // $("#NavBar").css("display","block")
            // $("#NavBar").addClass("animate__slideInDown")
            $(".generalNavBar").css({
                "position": "sticky",
                "top": "0px",
                "z-index": "9",
                "background-color": "black"
            })
        }
        if (window.scrollY <= 100) {
            // $("#NavBar").css("display","none")
            $(".generalNavBar").css("position", "relative")
        }
    })

    $(window).scroll(function () {
        if (window.scrollY >= 80) {
            $(".homeStickyNav").show()
            // $("#NavBar").css("display","block")
            // $("#NavBar").addClass("animate__slideInDown")
            $(".homeStickyNav").css({
                "position": "sticky",
                "top": "0px",
                "z-index": "9",
                "background-color": "black"
            })
        }
        if (window.scrollY <= 100) {
            $(".homeStickyNav").css({
                "position": "relative",
                "background-color": "transparent"
            })
        }
    })

    $(".modalShowerAddToCard").click(function (e) {
        e.preventDefault()
        $(this).parent().parent().next().next().toggleClass("d-none")
        $(this).parent().parent().next().next().toggleClass("d-block")
        $(this).parent().parent().next().next().children().removeClass("d-none")
        $(this).parent().parent().next().next().children().addClass("animate__zoomIn")
    })
    $(".modalClose").click(function (e) {
        e.preventDefault();
        $(this).parent().parent().toggleClass("d-block")
        $(this).parent().parent().toggleClass("d-none")
    })

    $(".modalSizeLi").click(function () {

        if (!$(this).hasClass("isSelectedSize")) {
            $(this).toggleClass("isSelectedSize");
        }
        $(this).siblings().removeClass("isSelectedSize")
        let sizeValue = $(this).attr("data-value")
        $(this).parent().parent().parent().children().first().children().first().children().first().html(sizeValue)

    })

    $(".modalColorLi").click(function (e) {
        e.preventDefault()
        if (!$(this).hasClass("isSelectedColor")) {
            $(this).toggleClass("isSelectedColor");
        }

        $(this).siblings().removeClass("isSelectedColor")
        let colorValue = $(this).attr("data-value")
        $(this).parent().parent().parent().children().first().children().first().children().first().html(colorValue)
    });

    $(".modalPlus").click(function (e) {
        e.preventDefault()

        $(this).siblings()[1].innerText++;


    })
    $(".modalMinus").click(function (e) {
        e.preventDefault()
        if ($(this).siblings()[0].innerText > 1) {
            $(this).siblings()[0].innerText--;
        } else {
            alert("Number of the products can't be lower than 1")
        }
    })
})