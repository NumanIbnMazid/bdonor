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

// go back button
$("button#go_back").on("click", function(e) {
  e.preventDefault();
  window.history.back();
});


// ripple-effect
$('button, .menu a, .to-ripple').rippleEffect();


// autocomplete modules starts =================================

// autocomplete handler
function AutoCompleteSelectHandler(event, ui) {
  var selectedObj = ui.item;
}

jQuery.ui.autocomplete.prototype._resizeMenu = function () {
  var ul = this.menu.element;
  ul.outerWidth(this.element.outerWidth());
}
$.extend($.ui.autocomplete.prototype.options, {
  open: function (event, ui) {
    $(this).autocomplete("widget").css({
      // "width": ($(this).width() + "px"),
      "max-height": "23%",
      "overflow-y": "auto",
      "overflow-x": "hidden",
      // "padding-right": "20px",
      "padding-left": "13px"
    });
  }
});

// autocomplete modules ends =================================


// accordian JS ==========================
$(document).ready(function () {
  $('.accordian-card-heading').on('click', function () {
    if ($(this).parents('.accordian-card').hasClass('open')) {
      $(this).parents('.accordian-card').find('.accordian-card-body').slideUp();
      $(this).parents('.accordian-card').removeClass('open');
    } else {
      $('.accordian-card-body').slideUp();
      $('.accordian-card').removeClass('open');

      $(this).parents('.accordian-card').find('.accordian-card-body').slideDown();
      $(this).parents('.accordian-card').addClass('open');
    }
  });
});
