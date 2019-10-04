$(document).ready(function () {
    $('#lightSlider, #donation_offers, #donation_requests').lightSlider({
        item: 4,
        loop: false,
        slideMove: 2,
        // rtl: true,
        // adaptiveHeight: true,
        slideMargin: 13,
        // loop: true,
        // vertical: true,
        // verticalHeight: 295,
        // vThumbWidth: 50,
        // thumbItem: 8,
        // thumbMargin: 4,
        // easing: 'cubic-bezier(0.25, 0, 0.25, 1)',
        // addClass: '',
        // mode: "slide",
        // useCSS: true,
        // speed: 600,
        pause: 2000,
        slideEndAnimation: true,
        keyPress: false,
        // controls: true,
        // prevHtml: '<span><</span>',
        // nextHtml: '<span>></span>',
        currentPagerPosition: 'middle',
        enableTouch: true,
        enableDrag: true,
        freeMove: true,
        swipeThreshold: 40,
        responsive: [{
                breakpoint: 800,
                settings: {
                    item: 2,
                    slideMove: 1,
                    slideMargin: 6,
                }
            },
            {
                breakpoint: 480,
                settings: {
                    item: 1,
                    slideMove: 1
                }
            }
        ]
    });
});

// $(document).ready(function () {
//     $('#donation_offers, #donation_requests').lightSlider({
//         item: 4,
//         loop: false,
//         slideMove: 2,
//         slideMargin: 13,
//         pause: 2000,
//         slideEndAnimation: true,
//         keyPress: false,
//         currentPagerPosition: 'middle',
//         enableTouch: true,
//         enableDrag: true,
//         freeMove: true,
//         swipeThreshold: 40,
//         responsive: [{
//                 breakpoint: 800,
//                 settings: {
//                     item: 2,
//                     slideMove: 1,
//                     slideMargin: 6,
//                 }
//             },
//             {
//                 breakpoint: 480,
//                 settings: {
//                     item: 1,
//                     slideMove: 1
//                 }
//             }
//         ]
//     });
// });