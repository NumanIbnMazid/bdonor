// scroll to top
$(window).scroll(function() {
  if ($(this).scrollTop() > 300) {
    $(".auto-scroll-to-top").addClass("visible");
  } else {
    $(".auto-scroll-to-top").removeClass("visible");
  }
});

$(".auto-scroll-to-top").click(function() {
  $("html, body").animate({ scrollTop: 0 }, 600);
});
