$(document).ready(function () {
    $(".owl-carousel").owlCarousel({
        items: 1,
        margin: 10,
        autoHeight: true,
        autoplay: true,
        autoplayTimeout: 5000,
        autoplayHoverPause: true,
        loop: false,
        center: true,
        mouseDrag: true,
        touchDrag: true,
        pullDrag: true,
        nav: true,
        rewind: true,
        smartSpeed: 250,
        responsiveRefreshRate: 200,
        // video: true,
        navText: ["<i class='fas fa-chevron-left mr-2'></i>", "<i class='fas fa-chevron-right ml-2'></i>"],
        // freeDrag: false,
        // videoHeight: 200,
        // videoWidth: 200,
        // stagePadding: false,
        // merge: false,
        // mergeFit: false,
        // autoWidth: false,
        // startPosition: 0,
    });
});

// <div class="owl-carousel">
//     .... content ....
// </div>