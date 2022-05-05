$(document).ready(function () {
    $('.myOwl').owlCarousel({
        loop: true,
        // margin: 10,
        nav: true,
        dots: false,
        responsive: {
            0: {
                items: 1
            },
            600: {
                items: 1
            },
            1000: {
                items: 1
            }
        }
    })
    $('.featured').owlCarousel({
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

    if ($(".featured .owl-item").hasClass("active")) {
        $(".featured .owl-item").siblings().addClass("d-flex justify-content-center")
    }

    // $(".brandImagesRow .brand").hover(function(){
    //     $(this).addClass("animate__bounceIn")
        
    // })
})