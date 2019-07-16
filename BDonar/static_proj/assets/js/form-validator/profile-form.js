// ===================== Profile Form JS ======================

var form = $("#profile_form");
var first_name = $("#profile_first_name");
var last_name = $("#profile_last_name");
var dob = $("#profile_dob");
var contact = $("#profile_contact");
var contactFake = $("#contactFake");
var address = $("#profile_address");
var location_fake_input = $("#location_fake_input");
var js_location_detect = $("#js_location_detect");
var location_result = $("#location_result");
// var detect_location = $("#detect_location");
var input_msg = $(".input-message");

// countryCode
var selectedDialCodeInitial = $(".selected-dial-code");
var countryCodeInitial = selectedDialCodeInitial.text();
var codesInitial = countryCodeInitial.split("+");
var contactCodeInitial = "+" + codesInitial[1];

function resetMessage() {
  input_msg.html("");
}


// Autocomplete starts---------------------------------------------
$(function () {
  // $("#profile_address").autocomplete({
  //   source: "/utils/autocomplete/address/",
  //   select: function (event, ui) { //item selected
  //     AutoCompleteSelectHandler(event, ui)
  //   },
  //   minLength: 2,
  // });
});

// Autocomplete ends---------------------------------------------

// force to enter only number 0-9
(function($) {
  $.fn.inputFilter = function(inputFilter) {
    return this.on(
      "input keydown keyup mousedown mouseup select contextmenu drop",
      function() {
        if (inputFilter(this.value)) {
          this.oldValue = this.value;
          this.oldSelectionStart = this.selectionStart;
          this.oldSelectionEnd = this.selectionEnd;
        } else if (this.hasOwnProperty("oldValue")) {
          this.value = this.oldValue;
          this.setSelectionRange(this.oldSelectionStart, this.oldSelectionEnd);
        }
      }
    );
  };
})(jQuery);

contact.inputFilter(function(value) {
  return /^\d*$/.test(value);
});

// default initialisation
$(document).ready(function() {
  // contact
  if (contact.val() == "") {
    contact.attr("placeholder", "1812345678");
    var contactPlaceholder = contact.attr("placeholder");
    contact.attr("maxlength", contactPlaceholder.length);
    contact.attr("minlength", contactPlaceholder.length);
  } else {
    contact.attr("placeholder", contact.val());
    var contactPlaceholder = contact.attr("placeholder");
    contact.attr("maxlength", contactPlaceholder.length);
    contact.attr("minlength", contactPlaceholder.length);
    contactFake.val(contactCodeInitial);
  }
});

// force to match the minimum and maximum length
contact.keypress(function(e) {
  var max = contactFake.attr("maxlength");
  if (e.which < 0x20) {
    // e.which < 0x20, then it's not a printable character
    // e.which === 0 - Not a character
    return; // Do nothing
  }
  if (this.value.length == max) {
    e.preventDefault();
  } else if (this.value.length > max) {
    // Maximum exceeded
    this.value = this.value.substring(0, max);
  }
});

// =========== intlTelInput Phone =============

// contact

contact.intlTelInput({
  initialCountry: "bd", //auto
  nationalMode: false,
  preferredCountries: ["bd", "us"],
  separateDialCode: true,
  formatOnDisplay: false
});

contact[0].addEventListener("open:countrydropdown", function() {
  contact.attr("maxlength", 15);
  contact.attr("minlength", 15);
});

contact[0].addEventListener("close:countrydropdown", function() {
  var selectedDialCode = $(".selected-dial-code");
  var countryCode = selectedDialCode.text();
  var codes = countryCode.split("+");
  var contactCode = "+" + codes[1];
  //   console.log(contactCode);
  contactFake.val(contactCode);
  var inputPlaceholder = contact.attr("placeholder").replace(/[- )(]/g, "");

  contact.val("");
  contact.attr("placeholder", inputPlaceholder);
  contact.attr("maxlength", inputPlaceholder.length);
  contact.attr("minlength", inputPlaceholder.length);

  contactFake.attr("maxlength", inputPlaceholder.length);
});

// date-time picker
$(document).ready(function() {
  function now() {
    var d = new Date();
    var month = d.getMonth() + 1;
    var day = d.getDate();
    var output =
      d.getFullYear() +
      "/" +
      (month < 10 ? "0" : "") +
      month +
      "/" +
      (day < 10 ? "0" : "") +
      day;
    return output;
  }

  dob.datetimepicker({
    timepicker: false,
    format: "Y-m-d",
    maxDate: now(),
    validateOnBlur: true
  });
});

form.submit(function(event) {
  if (contact.val() != "") {
    if (contact.val().length != contact.attr("placeholder").length) {
      event.preventDefault();
      $("#contact_msg").html("Please enter a valid contact number.");
    } else {
      return true;
    }
  }
  return true;
});

// preventing form from autocomplete
$(document).ready(function() {
  $(document).on("focus", ":input", function() {
    $(this).attr("autocomplete", "off");
  });
});


// Map Detect User Current Location
(function ($, google) {
  js_location_detect.on("click", function (e) {
    $.geolocate({
        loading: "detecting....",
        formatted_address: true,
        name: "long_name", // "short_name", "long_name"
        delimeter: ", ",
        enableHighAccuracy: true,
        timeout: 5000,
        maximumAge: 0
      })
      .done(function (result) {
        if ((result != "Could not an address for your location.") && (result != "")) {
          location_fake_input.removeClass("hidden");
          location_fake_input.val(result);
          $("#location_detect_msg").html("Is that right location?").css('color', '#1f4787');
          $("#location_confirm_btn").removeClass("hidden");
        } else {
          location_fake_input.val("");
          location_fake_input.addClass("hidden");
          $("#location_detect_msg").html("Could not detect your locaton.").css('color', '#B93232');
          $("#location_confirm_btn").addClass("hidden");
        }
      });
  });

  // try again
  $("#try_again").on("click", function (e) {
    location_fake_input.val("detecting.....");
    $.geolocate({
        loading: "detecting....",
        formatted_address: true,
        name: "long_name", // "short_name", "long_name"
        delimeter: ", ",
        enableHighAccuracy: true,
        timeout: 5000,
        maximumAge: 0
      })
      .done(function (result) {
        if ((result != "Could not an address for your location.") && (result != "")) {
          location_fake_input.removeClass("hidden");
          location_fake_input.val(result);
          $("#location_detect_msg").html("Is that right location?").css('color', '#1f4787');
          $("#location_confirm_btn").removeClass("hidden");
        } else {
          location_fake_input.val("");
          location_fake_input.addClass("hidden");
          $("#location_detect_msg").html("Could not detect your locaton.").css('color', '#B93232');
          $("#location_confirm_btn").addClass("hidden");
        }
      });
  });

})(jQuery, google);