// ===================== Donation Form JS ======================
var form = $("#donation_respond_form");
var submitBtn = $("#submitBtn");
var contact_input = $("#donation_contact_input");
var contact_group = $("#donation_contact_input-group");
var message_input = $("#donation_message_input");
var message_group = $("#donation_message_input-group");
var inputStyle = contact_input.attr("style");
var contactFake = $("#contactFake");
var form_error = $(".form-error");
var error_group = $(".error-group");

// countryCode
var selectedDialCodeInitial = $(".selected-dial-code");
var countryCodeInitial = selectedDialCodeInitial.text();
var codesInitial = countryCodeInitial.split("+");
var contactCodeInitial = "+" + codesInitial[1];

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

contact_input.inputFilter(function(value) {
  return /^\d*$/.test(value);
});


// default initialisation
$(document).ready(function() {
  // contact
  if (contact_input.val() == "") {
    contact_input.attr("placeholder", "1812345678");
    var contactPlaceholder = contact_input.attr("placeholder");
    contact_input.attr("maxlength", contactPlaceholder.length);
    contact_input.attr("minlength", contactPlaceholder.length);
  } else {
    contact_input.attr("placeholder", contact_input.val());
    var contactPlaceholder = contact_input.attr("placeholder");
    contact_input.attr("maxlength", contactPlaceholder.length);
    contact_input.attr("minlength", contactPlaceholder.length);
    contactFake.val(contactCodeInitial);
  }
});


function resetMessage() {
  $(".input-message").html("");
}


// =========== intlTelInput Phone =============

contact_input.intlTelInput({
  initialCountry: "bd", //auto
  nationalMode: false,
  preferredCountries: ["bd", "us"],
  separateDialCode: true,
  formatOnDisplay: false
});

// contact 1
contact_input[0].addEventListener("open:countrydropdown", function () {
  contact_input.attr("maxlength", 15);
  contact_input.attr("minlength", 15);
});

contact_input[0].addEventListener("close:countrydropdown", function () {
  var selectedDialCode = $(".selected-dial-code");
  var countryCode = selectedDialCode.text();
  // console.log(countryCode);
  var codes = countryCode.split("+");
  // console.log(codes);
  // console.log(codes[1]);
  // console.log(codes[2]);
  // console.log(codes[3]);
  var contact1code = "+" + codes[1];
  contactFake.val(contact1code);
  var inputPlaceholder = contact_input
    .attr("placeholder")
    .replace(/[- )(]/g, "");

  contact_input.val("");
  contact_input.attr("placeholder", inputPlaceholder);
  contact_input.attr("maxlength", inputPlaceholder.length);
  contact_input.attr("minlength", inputPlaceholder.length);

  contactFake.attr("maxlength", inputPlaceholder.length);
});

// force to match the minimum and maximum length
contact_input.keypress(function (e) {
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


form.submit(function(event) {
  if (contact_input.val() != "") {
    if (contact_input.val().length != contact_input.attr("placeholder").length) {
      event.preventDefault();
      $("#contact_msg").html("Please enter a valid contact number.");
    } else {
      return true;
    }
  }
  return true;
});

// preventing form from autocomplete
$(document).ready(function () {
  $(document).on("focus", ":input", function () {
    $(this).attr("autocomplete", "off");
  });
});