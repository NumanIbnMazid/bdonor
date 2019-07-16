// ===================== Donation Form JS ======================
var page_title = $("#page_title");
var form = $("#offer_create_form");
var submitBtn = $("#submitBtn");
var message_holder = $("#message_holder");
var advanced = $("#advanced");
var hide_advanced = $("#hide_advanced");
var type_input = $("#donation_type_input");
var tissue_name_input = $("#donation_tissue_name_input");
var tissue_name_group = $("#donation_tissue_name_input-group");
var contact_input = $("#donation_contact_input");
var contact_group = $("#donation_contact_input-group");
var contact2_input = $("#donation_contact2_input");
var contact2_group = $("#donation_contact2_input-group");
var contact3_input = $("#donation_contact3_input");
var contact3_group = $("#donation_contact3_input-group");
var blood_group_input = $("#donation_blood_group_input");
var blood_group_group = $("#donation_blood_group_input-group");
var blood_bag_input = $("#donation_blood_bag_input");
var blood_bag_group = $("#donation_blood_bag_input-group");
var organ_name_input = $("#donation_organ_name_input");
var organ_name_group = $("#donation_organ_name_input-group");
var tissue_name_input = $("#donation_tissue_name_input");
var tissue_name_group = $("#donation_tissue_name_input-group");
var quantity_input = $("#donation_quantity_input");
var quantity_group = $("#donation_quantity_input-group");
var hospital_input = $("#donation_hospital_input");
var hospital_group = $("#donation_hospital_input-group");
var details_input = $("#donation_details_input");
var details_group = $("#donation_details_input-group");
var details_fake_input = $("#donation_details_fake_input");
var details_fake_group = $("#donation_details_fake_input-group");
var preferred_date_input = $("#donation_preferred_date_input");
var preferred_date_group = $("#donation_preferred_date_input-group");
var preferred_date_from_input = $("#donation_preferred_date_from_input");
var preferred_date_from_group = $("#donation_preferred_date_from_input-group");
var preferred_date_to_input = $("#donation_preferred_date_to_input");
var preferred_date_to_group = $("#donation_preferred_date_to_input-group");
var location_input = $("#donation_location_input");
var location_fake_input = $("#location_fake_input");
var js_location_detect = $("#js_location_detect");
var location_result = $("#location_result");
var location_group = $("#donation_location_input-group");
var priority_input = $("#donation_priority_input");
var priority_group = $("#donation_priority_input-group");
var publication_status_input = $("#donation_publication_status_input");
var publication_status_group = $("#donation_publication_status_input-group");
var invisible_input_group = $(".invisible-input-group");
var special_input_group = $(".special-input-group");
var add_second_contact = $("#add_second_contact");
var add_third_contact = $("#add_third_contact");
var hide_contact2 = $("#hide_contact2");
var hide_contact3 = $("#hide_contact3");
var field_priority = $(".field_priority");
var inputStyle = contact_input.attr("style");
var contactFake = $("#contactFake");
var contact2Fake = $("#contact2Fake");
var contact3Fake = $("#contact3Fake");
var set_date_between = $("#set_date_between");
var hide_set_date_between = $("#hide_set_date_between");
var datetime = $("#datetime");
var date_with_time = $("#date_with_time");
var date_without_time = $("#date_without_time");
var advanced_editing = $("#advanced_editing");
var basic_editing = $("#basic_editing");
var detect_location = $("#detect_location");
var form_error = $(".form-error");
var special_input = $(".special-input");
var error_group = $(".error-group");

// countryCode
var selectedDialCodeInitial = $(".selected-dial-code");
var countryCodeInitial = selectedDialCodeInitial.text();
var codesInitial = countryCodeInitial.split("+");

var contactCodeInitial = "+" + codesInitial[1];
var contact2CodeInitial = "+" + codesInitial[2];
var contact3CodeInitial = "+" + codesInitial[3];

function resetMessage() {
  $(".input-message").html("");
  $(".form-error-div").html("");
  $(".form-group").removeClass("border-danger-1");
}

// Check if string is HTML or Not
function isHTML(str) {
  var a = document.createElement("div");
  a.innerHTML = str;

  for (var c = a.childNodes, i = c.length; i--;) {
    if (c[i].nodeType == 1) return true;
  }

  return false;
}

// console.log(moment().format('MMMM Do YYYY, h:mm:ss a'));



// Autocomplete starts---------------------------------------------
$(function () {
  // var input_width = $("#donation_location_input").width();
  // $("#donation_location_input").autocomplete({
  //   source: "/utils/autocomplete/address/",
  //   appendTo: '#menu-container',
  //   select: function (event, ui) { //item selected
  //     AutoCompleteSelectHandler(event, ui)
  //   },
  //   minLength: 2,
  // });
});

$(function () {
  $("#donation_hospital_input").autocomplete({
    source: "/utils/autocomplete/hospital/",
    select: function (event, ui) { //item selected
      AutoCompleteSelectHandler(event, ui)
    },
    minLength: 2,
  });
});

// Autocomplete ends---------------------------------------------

// force to enter only number 0-9
(function ($) {
  $.fn.inputFilter = function (inputFilter) {
    return this.on(
      "input keydown keyup mousedown mouseup select contextmenu drop",
      function () {
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

contact_input.inputFilter(function (value) {
  return /^\d*$/.test(value);
});
contact2_input.inputFilter(function (value) {
  return /^\d*$/.test(value);
});
contact3_input.inputFilter(function (value) {
  return /^\d*$/.test(value);
});
// blood_bag_input.inputFilter(function(value) {
//   return /^\d*$/.test(value);
// });

// ends force to enter only number 0-9

// force to enter only number between 100
if ((page_title.val() == "Create donation offer") || page_title.val() == "Update donation offer") {
  // blood_bag_input.val(1);
  blood_bag_input.inputFilter(function (value) {
    return /^\d*$/.test(value) && (value === "" || parseInt(value) <= 1);
  });
}
else{
  blood_bag_input.inputFilter(function (value) {
    return /^\d*$/.test(value) && (value === "" || parseInt(value) <= 100);
  });
}
quantity_input.inputFilter(function (value) {
  return /^\d*$/.test(value) && (value === "" || parseInt(value) <= 2);
});
// ends force to enter only number between 100

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

contact2_input.keypress(function (e) {
  var max = contact2Fake.attr("maxlength");
  if (e.which < 0x20) {
    return;
  }
  if (this.value.length == max) {
    e.preventDefault();
  } else if (this.value.length > max) {
    this.value = this.value.substring(0, max);
  }
});

contact3_input.keypress(function (e) {
  var max = contact3Fake.attr("maxlength");
  if (e.which < 0x20) {
    return;
  }
  if (this.value.length == max) {
    e.preventDefault();
  } else if (this.value.length > max) {
    this.value = this.value.substring(0, max);
  }
});

// ends force to match the minimum and maximum length

// default initialisation
$(document).ready(function () {
  if (type_input.val() == 0){
    $("#blood_group_priority").addClass("text-info");
    $("#blood_group_priority").html("(required)");
    blood_group_input.attr("required", true);
    $("#blood_bag_priority").addClass("text-info");
    $("#blood_bag_priority").html("(required)");
    blood_bag_input.attr("required", true);
  }
  if (type_input.val() == 1){
    $("#organ_name_priority").addClass("text-info");
    $("#organ_name_priority").html("(required)");
    organ_name_input.attr("required", true);
    $("#quantity_priority").addClass("text-info");
    $("#quantity_priority").html("(required)");
    quantity_input.attr("required", true);
  }
  if (type_input.val() == 2) {
    $("#tissue_name_priority").addClass("text-info");
    $("#tissue_name_priority").html("(required)");
    tissue_name_input.attr("required", true);
    // $("#quantity_priority").addClass("text-info");
    // $("#quantity_priority").html("(required)");
    // quantity_input.attr("required", true);
  }
  if (organ_name_input.val() == "Heart") {
    quantity_input.val(1);
    quantity_input.attr("disabled", true);
  } else {
    quantity_input.attr("disabled", false);
    // quantity_input.inputFilter(function (value) {
    //   return /^\d*$/.test(value) && (value === "" || parseInt(value) <= 2);
    // });
  }
  // details editor
  if (details_input.val() != "") {
    if (isHTML(details_input.val()) == true) {
      for (instance in CKEDITOR.instances) {
        CKEDITOR.instances[instance].setData(details_input.val());
      }
      details_input.val("");
      details_fake_group.removeClass("hidden");
      details_group.addClass("hidden");
      advanced_editing.addClass("hidden");
      basic_editing.removeClass("hidden");
    } else {
      for (instance in CKEDITOR.instances) {
        CKEDITOR.instances[instance].setData(" ");
      }
      details_fake_group.addClass("hidden");
      details_group.removeClass("hidden");
      advanced_editing.removeClass("hidden");
      basic_editing.addClass("hidden");
    }
  }
  // contact 1
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

  // contact_input.attr("placeholder", "1812345678");
  // var contactPlaceholder = contact_input.attr("placeholder");
  // contact_input.attr("maxlength", contactPlaceholder.length);
  // contact_input.attr("minlength", contactPlaceholder.length);

  // contact 2
  if (contact2_input.val() == "") {
    contact2_input.attr("style", inputStyle);
    contact2_input.attr("placeholder", "1812345678");
    var contact2Placeholder = contact2_input.attr("placeholder");
    contact2_input.attr("maxlength", contact2Placeholder.length);
    contact2_input.attr("minlength", contact2Placeholder.length);
  } else {
    contact2_input.attr("style", inputStyle);
    contact2_input.attr("placeholder", contact2_input.val());
    var contact2Placeholder = contact2_input.attr("placeholder");
    contact2_input.attr("maxlength", contact2Placeholder.length);
    contact2_input.attr("minlength", contact2Placeholder.length);
    contact2Fake.val(contact2CodeInitial);
  }

  // contact2_input.attr("style", inputStyle);
  // contact2_input.attr("placeholder", "1812345678");
  // var contact2Placeholder = contact2_input.attr("placeholder");
  // contact2_input.attr("maxlength", contact2Placeholder.length);
  // contact2_input.attr("minlength", contact2Placeholder.length);

  // contact 3
  if (contact3_input.val() == "") {
    contact3_input.attr("style", inputStyle);
    contact3_input.attr("placeholder", "1812345678");
    var contact3Placeholder = contact3_input.attr("placeholder");
    contact3_input.attr("maxlength", contact3Placeholder.length);
    contact3_input.attr("minlength", contact3Placeholder.length);
  } else {
    contact3_input.attr("style", inputStyle);
    contact3_input.attr("placeholder", contact3_input.val());
    var contact3Placeholder = contact3_input.attr("placeholder");
    contact3_input.attr("maxlength", contact3Placeholder.length);
    contact3_input.attr("minlength", contact3Placeholder.length);
    contact3Fake.val(contact3CodeInitial);
  }

  // contact3_input.attr("style", inputStyle);
  // contact3_input.attr("placeholder", "1812345678");
  // var contact3Placeholder = contact3_input.attr("placeholder");
  // contact3_input.attr("maxlength", contact3Placeholder.length);
  // contact3_input.attr("minlength", contact3Placeholder.length);

  // functions
  advanced_editing.click(function () {
    // details_input.val("");
    details_fake_group.removeClass("hidden");
    details_group.addClass("hidden");
    advanced_editing.addClass("hidden");
    basic_editing.removeClass("hidden");
  });
  basic_editing.click(function () {
    // details_fake_input.val("");
    // for (instance in CKEDITOR.instances) {
    //   CKEDITOR.instances[instance].setData(" ");
    // }
    details_fake_group.addClass("hidden");
    details_group.removeClass("hidden");
    advanced_editing.removeClass("hidden");
    basic_editing.addClass("hidden");
  });
  advanced.click(function () {
    special_input_group.removeClass("hidden");
    preferred_date_from_group.addClass("hidden");
    preferred_date_to_group.addClass("hidden");
    advanced.addClass("hidden");
    if (set_date_between.hasClass("hidden")) {
      set_date_between.removeClass("hidden");
    } else {
      set_date_between.addClass("hidden");
      preferred_date_from_group.removeClass("hidden");
      preferred_date_to_group.removeClass("hidden");
    }
    hide_advanced.removeClass("hidden");
    if ((page_title.val() == "Create donation offer") || page_title.val() == "Update donation offer") {
      $("#donation_priority_input-group").addClass("hidden");
    }
  });
  hide_advanced.click(function () {
    special_input_group.addClass("hidden");
    advanced.removeClass("hidden");
    if (set_date_between.hasClass("hidden")) {
      preferred_date_from_group.addClass("hidden");
      preferred_date_to_group.addClass("hidden");
    }
    hide_advanced.addClass("hidden");
  });
  hide_contact2.click(function () {
    contact3_group.addClass("hidden");
    contact2_group.addClass("hidden");
    contact3_input.val("");
    contact2_input.val("");
    if (
      contact_input.val().length == contact_input.attr("placeholder").length
    ) {
      add_second_contact.removeClass("hidden");
    }
  });
  hide_contact3.click(function () {
    contact3_group.addClass("hidden");
    contact3_input.val("");
    if (
      contact2_input.val().length == contact_input.attr("placeholder").length
    ) {
      add_third_contact.removeClass("hidden");
    }
  });
  add_second_contact.click(function () {
    if (
      contact2_input.val().length < contact_input.attr("placeholder").length
    ) {
      add_third_contact.addClass("hidden");
    }
    if (
      contact_input.val().length == contact_input.attr("placeholder").length
    ) {
      resetMessage();
      add_second_contact.addClass("hidden");
      contact2_group.removeClass("hidden");
    }
  });
  if (contact_input.val().length == contact_input.attr("placeholder").length) {
    add_second_contact.removeClass("hidden");
  }

  // date between
  // Dynamic Preview of Set Date Between
  // if (preferred_date_from_input.val() == "" || preferred_date_to_input.val() == "") {
  //   preferred_date_from_group.addClass('hidden');
  //   preferred_date_to_group.addClass('hidden');
  //   set_date_between.removeClass('hidden');
  //   hide_set_date_between.addClass('hidden');
  //   preferred_date_from_input.val("");
  //   preferred_date_to_input.val("");
  // } else {
  //   preferred_date_from_group.removeClass('hidden');
  //   preferred_date_to_group.removeClass('hidden');
  //   set_date_between.addClass('hidden');
  //   hide_set_date_between.removeClass('hidden');
  // }
  if (preferred_date_from_group.hasClass("hidden") == true) {
    set_date_between.removeClass("hidden");
    hide_set_date_between.addClass("hidden");
  } else {
    set_date_between.addClass("hidden");
    hide_set_date_between.removeClass("hidden");
  }
  set_date_between.click(function () {
    preferred_date_from_group.removeClass("hidden");
    preferred_date_to_group.removeClass("hidden");
    set_date_between.addClass("hidden");
    hide_set_date_between.removeClass("hidden");
  });
  hide_set_date_between.click(function () {
    preferred_date_from_group.addClass("hidden");
    preferred_date_to_group.addClass("hidden");
    preferred_date_from_input.val("");
    preferred_date_to_input.val("");
    hide_set_date_between.addClass("hidden");
    set_date_between.removeClass("hidden");
  });
  // Date Time
  if (preferred_date_input.val() != "") {
    preferred_date_moment = moment(preferred_date_input.val()).format(
      "hh:mm:ss"
    );
    // console.log((preferred_date_input.val()).length);
    if (preferred_date_input.val().length <= 11) {
      // if (preferred_date_moment != "00:00:00") {
      date_without_time.addClass("hidden");
      date_with_time.removeClass("hidden");
      datetime.val(false);
    } else {
      date_without_time.removeClass("hidden");
      date_with_time.addClass("hidden");
      datetime.val(true);
    }
  }
  date_with_time.click(function () {
    date_with_time.addClass("hidden");
    date_without_time.removeClass("hidden");
    if (preferred_date_input.val() != "") {
      preferred_date_input.val(
        moment(preferred_date_input.val()).format("YYYY-MM-DD hh:mm")
      );
    }
    if (preferred_date_from_input.val() != "") {
      preferred_date_from_input.val(
        moment(preferred_date_from_input.val()).format("YYYY-MM-DD hh:mm")
      );
    }
    if (preferred_date_to_input.val() != "") {
      preferred_date_to_input.val(
        moment(preferred_date_to_input.val()).format("YYYY-MM-DD hh:mm")
      );
    }
    // preferred_date_input.val("");
    // preferred_date_from_input.val("");
    // preferred_date_to_input.val("");
    datetime.val(true);
  });
  date_without_time.click(function () {
    date_without_time.addClass("hidden");
    date_with_time.removeClass("hidden");
    if (preferred_date_input.val() != "") {
      preferred_date_input.val(
        moment(preferred_date_input.val()).format("YYYY-MM-DD")
      );
    }
    if (preferred_date_from_input.val() != "") {
      preferred_date_from_input.val(
        moment(preferred_date_from_input.val()).format("YYYY-MM-DD")
      );
    }
    if (preferred_date_to_input.val() != "") {
      preferred_date_to_input.val(
        moment(preferred_date_to_input.val()).format("YYYY-MM-DD")
      );
    }
    // preferred_date_input.val("");
    // preferred_date_from_input.val("");
    // preferred_date_to_input.val("");
    datetime.val(false);
  });
});

// ends default initialisation


// =========== intlTelInput Phone =============

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

  contact3_group.addClass("hidden");
  contact2_group.addClass("hidden");
  add_second_contact.addClass("hidden");
  contact3_input.val("");
  contact2_input.val("");
});

// contact 2
contact2_input[0].addEventListener("open:countrydropdown", function () {
  contact2_input.attr("maxlength", 15);
  contact2_input.attr("minlength", 15);
});

contact2_input[0].addEventListener("close:countrydropdown", function () {
  var selectedDialCode = $(".selected-dial-code");
  var countryCode = selectedDialCode.text();
  var codes = countryCode.split("+");
  var contact2code = "+" + codes[2];
  contact2Fake.val(contact2code);
  var inputPlaceholder = contact2_input
    .attr("placeholder")
    .replace(/[- )(]/g, "");

  contact2_input.val("");
  contact2_input.attr("placeholder", inputPlaceholder);
  contact2_input.attr("maxlength", inputPlaceholder.length);
  contact2_input.attr("minlength", inputPlaceholder.length);

  contact2Fake.attr("maxlength", inputPlaceholder.length);

  contact3_group.addClass("hidden");
  add_third_contact.addClass("hidden");
  contact3_input.val("");
});

// contact 3
contact3_input[0].addEventListener("open:countrydropdown", function () {
  contact3_input.attr("maxlength", 15);
  contact3_input.attr("minlength", 15);
});

contact3_input[0].addEventListener("close:countrydropdown", function () {
  var selectedDialCode = $(".selected-dial-code");
  var countryCode = selectedDialCode.text();
  var codes = countryCode.split("+");
  var contact3code = "+" + codes[3];
  contact3Fake.val(contact3code);
  var inputPlaceholder = contact3_input
    .attr("placeholder")
    .replace(/[- )(]/g, "");

  contact3_input.val("");
  contact3_input.attr("placeholder", inputPlaceholder);
  contact3_input.attr("maxlength", inputPlaceholder.length);
  contact3_input.attr("minlength", inputPlaceholder.length);

  contact3Fake.attr("maxlength", inputPlaceholder.length);
});

// submitBtn.click(function() {
//   console.log(selectedDialCode.text());
// });

// ================== /intlTelInput ===================

// --- type select function ---
function typeFunction() {
  resetMessage();
  if (type_input.val() == 0) {
    tissue_name_group.addClass("hidden");
    organ_name_group.addClass("hidden");
    blood_group_group.removeClass("hidden");
    blood_bag_group.removeClass("hidden");
    hospital_group.removeClass("hidden");
    // $("#blood_warning").removeClass("hidden");
    $("#blood_accordian").removeClass("hidden");
    $("#organ_accordian").addClass("hidden");
    $("#blood_group_priority").html("(required)");
    $("#blood_group_priority").addClass("text-info");
    blood_group_input.attr("required", true);
    $("#blood_bag_priority").html("(required)");
    $("#blood_bag_priority").addClass("text-info");
    if ((page_title.val() != "Create donation offer") || page_title.val() != "Update donation offer") {
      blood_bag_input.attr("required", true);
    }
    organ_name_input.attr("required", false);
    tissue_name_input.attr("required", false);
    quantity_input.attr("required", false);
    quantity_group.addClass("hidden");
    quantity_input.val("");
    tissue_name_input.val("");
    organ_name_input.val("");
    if ((page_title.val() == "Create donation offer") || page_title.val() == "Update donation offer") {
      blood_bag_input.prop('disabled', true);
      // blood_bag_group.addClass("hidden");
      blood_bag_input.val(1);
    }
  } else if (type_input.val() == 1) {
    tissue_name_group.addClass("hidden");
    organ_name_group.removeClass("hidden");
    hospital_group.removeClass("hidden");
    $("#blood_accordian").addClass("hidden");
    $("#organ_accordian").removeClass("hidden");
    $("#blood_warning").addClass("hidden");
    $("#organ_name_priority").html("(required)");
    $("#organ_name_priority").addClass("text-info");
    blood_group_input.attr("required", false);
    blood_bag_input.attr("required", false);
    organ_name_input.attr("required", true);
    tissue_name_input.attr("required", false);
    blood_group_group.addClass("hidden");
    blood_bag_group.addClass("hidden");
    $("#quantity_priority").html("(required)");
    $("#quantity_priority").addClass("text-info");
    quantity_input.attr("required", true);
    quantity_group.removeClass("hidden");
    $("#blood_warning_simple").addClass("hidden");
    quantity_input.val(1);
    tissue_name_input.val("");
    blood_group_input.val("");
    blood_bag_input.val("");
  } 
  else if (type_input.val() == 2) {
    tissue_name_group.removeClass("hidden");
    $("#tissue_name_priority").html("(required)");
    $("#tissue_name_priority").addClass("text-info");
    blood_group_input.attr("required", false);
    blood_bag_input.attr("required", false);
    organ_name_input.attr("required", false);
    tissue_name_input.attr("required", true);
    organ_name_group.addClass("hidden");
    blood_group_group.addClass("hidden");
    blood_bag_group.addClass("hidden");
    hospital_group.addClass("hidden");
    $("#blood_accordian").addClass("hidden");
    $("#organ_accordian").removeClass("hidden");
    $("#blood_warning").addClass("hidden");
    quantity_input.attr("required", false);
    quantity_group.addClass("hidden");
    $("#blood_warning_simple").addClass("hidden");
    quantity_input.val("");
    organ_name_input.val("");
    blood_group_input.val("");
    blood_bag_input.val("");
    hospital_input.val("");
  } else {
    tissue_name_group.addClass("hidden");
    organ_name_group.addClass("hidden");
    blood_group_group.addClass("hidden");
    blood_bag_group.addClass("hidden");
    hospital_group.addClass("hidden");
    $("#blood_accordian").addClass("hidden");
    $("#organ_accordian").addClass("hidden");
    $("#blood_warning").addClass("hidden");
    quantity_group.addClass("hidden");
    $("#blood_warning_simple").removeClass("hidden");
    quantity_input.val("");
    tissue_name_input.val("");
    organ_name_input.val("");
    blood_group_input.val("");
    blood_bag_input.val("");
    hospital_input.val("");
  }
}

$(contact_input).keyup(function () {
  resetMessage();
  var $this = $(this);
  var contactValue = $this.val();
  if (contactValue.length == contact_input.attr("placeholder").length) {
    if (contact2_group.hasClass("hidden") == true) {
      add_second_contact.removeClass("hidden");
    }
    add_second_contact.click(function () {
      if (
        contact_input.val().length == contact_input.attr("placeholder").length
      ) {
        resetMessage();
        add_second_contact.addClass("hidden");
        contact2_group.removeClass("hidden");
      } else {
        $("#contact_msg").html("Please enter first contact.");
      }
    });
  } else {
    contact2_input.val("");
    contact3_input.val("");
    add_second_contact.addClass("hidden");
    contact2_group.addClass("hidden");
    contact3_group.addClass("hidden");
  }
});

$(contact2_input).keyup(function () {
  resetMessage();
  var $this = $(this);
  var contact2Value = $this.val();
  if (contact2Value.length == contact2_input.attr("placeholder").length) {
    if (contact3_group.hasClass("hidden") == true) {
      add_third_contact.removeClass("hidden");
    }
    add_third_contact.click(function () {
      if (
        contact2_input.val().length == contact2_input.attr("placeholder").length
      ) {
        resetMessage();
        add_third_contact.addClass("hidden");
        contact3_group.removeClass("hidden");
      } else {
        $("#contact2_msg").html("Please enter second contact.");
      }
    });
  } else {
    contact3_input.val("");
    add_third_contact.addClass("hidden");
    contact3_group.addClass("hidden");
  }
});

$(contact3_input).keyup(function () {
  resetMessage();
});

// date-time picker
$(document).ready(function () {
  // var allowTime = datetime.val();
  // console.log(allowTime);
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

  preferred_date_input.datetimepicker({
    onShow: function (ct) {
      var allowTime = JSON.parse(datetime.val());
      if (allowTime == true) {
        this.setOptions({
          timepicker: true,
          format: "Y-m-d H:i",
          allowTimes: [
            // '11:00', '13:00', '15:00',
            // '16:00', '18:00', '19:00', '20:00'
            "01:00",
            "02:00",
            "03:00",
            "04:00",
            "05:00",
            "06:00",
            "07:00",
            "08:00",
            "09:00",
            "10:00",
            "11:00",
            "12:00",
            "13:00",
            "14:00",
            "15:00",
            "16:00",
            "17:00",
            "18:00",
            "19:00",
            "20:00",
            "21:00",
            "22:00",
            "23:00",
            // "23:50"
          ]
        });
      } else {
        this.setOptions({
          timepicker: false,
          format: "Y-m-d"
        });
      }
    },
    // mask:'9999/19/39',
    // format: "Y-m-d H:i",
    // formatDate:'Y/m/d',
    // timepicker:false,
    minDate: now(),
    // maxDate: next(),
    // minTime:'11:00',
    // datepicker:false,
    validateOnBlur: true
    // closeOnDateSelect:true,
    // closeOnWithoutClick: false,
    // todayButton: true,
    // hours12: false,
    // yearStart: 1950,
    // yearEnd: 2050,
    // value:'12:00',
    // inline:true,
    // weeks:true,
    // theme:'dark',
    // lang:'en',
    // i18n:{de:{
    //   months:[
    //   'January','February','March','April','May','June','July','August','September','October','November','December'
    //   ],
    //   dayOfWeek:["So.", "Mo", "Tu", "We", "Th", "Fr", "Sa."]
    // }},
    // startDate:'+1971/05/01',
    // format:'unixtime',
    // allowTimes: [
    // '11:00', '13:00', '15:00',
    // '16:00', '18:00', '19:00', '20:00'
    // ]
    // weekends:['01.01.2014','02.01.2014','03.01.2014','04.01.2014','05.01.2014','06.01.2014'],
    // onChangeDateTime:function(dp,$input){
    //   alert($input.val())
    // },
    // onShow:function(dp,$input){
    //   console.log(datetime.val());
    //   timepicker:datetime.val();
    // },
    // onGenerate:function( ct ){
    //   jQuery(this).find('.xdsoft_date')
    //     .toggleClass('xdsoft_disabled');
    // },
  });
  preferred_date_from_input.datetimepicker({
    onShow: function (ct) {
      var allowTime = JSON.parse(datetime.val());
      if (allowTime == true) {
        this.setOptions({
          timepicker: true,
          format: "Y-m-d H:i",
          allowTimes: [
            "01:00",
            "02:00",
            "03:00",
            "04:00",
            "05:00",
            "06:00",
            "07:00",
            "08:00",
            "09:00",
            "10:00",
            "11:00",
            "12:00",
            "13:00",
            "14:00",
            "15:00",
            "16:00",
            "17:00",
            "18:00",
            "19:00",
            "20:00",
            "21:00",
            "22:00",
            "23:00",
            // "23:50"
          ]
        });
      } else {
        this.setOptions({
          timepicker: false,
          format: "Y-m-d"
        });
      }
    },
    // format: "Y-m-d H:i",
    minDate: now(),
    validateOnBlur: true
  });
  preferred_date_to_input.datetimepicker({
    onShow: function (ct) {
      var allowTime = JSON.parse(datetime.val());
      if (allowTime == true) {
        this.setOptions({
          timepicker: true,
          format: "Y-m-d H:i",
          allowTimes: [
            "01:00",
            "02:00",
            "03:00",
            "04:00",
            "05:00",
            "06:00",
            "07:00",
            "08:00",
            "09:00",
            "10:00",
            "11:00",
            "12:00",
            "13:00",
            "14:00",
            "15:00",
            "16:00",
            "17:00",
            "18:00",
            "19:00",
            "20:00",
            "21:00",
            "22:00",
            "23:00",
            // "23:50"
          ]
        });
      } else {
        this.setOptions({
          timepicker: false,
          format: "Y-m-d"
        });
      }
    },
    // format: "Y-m-d H:i",
    minDate: now(),
    validateOnBlur: true
  });
});


function organFunction() {
  resetMessage();
  if (organ_name_input.val() == "Heart") {
    quantity_input.val(1);
    quantity_input.attr("disabled", true);
  }
  else if (organ_name_input.val() == "Liver") {
    quantity_input.val(1);
    quantity_input.attr("disabled", true);
  }
  else{
    quantity_input.attr("disabled", false);
    // quantity_input.inputFilter(function (value) {
    //   return /^\d*$/.test(value) && (value === "" || parseInt(value) <= 2);
    // });
  }
}

function getValue(input) {
  var resultValue;
  resultValue = input.val();
  if (input.attr('name') == 'type') {
    if (input.val() == "0") {
      if ((page_title.val() == "Create donation offer") || page_title.val() == "Update donation offer") {
        var html = ("Blood <br> <span class='text-dark'>Post Title:</span> I want to donate Blood.");
      }
      else{
        var html = ("Blood <br> <span class='text-dark'>Post Title:</span> I need Blood donor.");
      }
      resultValue = html;
    }
    if (input.val() == "1") {
      // resultValue = "Organ";
      if ((page_title.val() == "Create donation offer") || page_title.val() == "Update donation offer") {
        var html = ("Organ <br> <span class='text-dark'>Post Title:</span> I want to donate Organ.");
      }
      else{
        var html = ("Organ <br> <span class='text-dark'>Post Title:</span> I need Organ donor.");
      }
      resultValue = html;
    }
    if (input.val() == "2") {
      // resultValue = "Tissue";
      if ((page_title.val() == "Create donation offer") || page_title.val() == "Update donation offer") {
        var html = ("Tissue <br> <span class='text-dark'>Post Title:</span> I want to donate Tissue.");
      }
      else{
        var html = ("Tissue <br> <span class='text-dark'>Post Title:</span> I need Tissue donor.");
      }
      resultValue = html;
    }
  }
  if (input.attr('name') == 'contact_privacy') {
    if (input.val() == "0") {
      resultValue = "Public";
    }
    if (input.val() == "1") {
      resultValue = "Private";
    }
  }
  if (input.attr('name') == 'priority') {
    if (input.val() == "0") {
      resultValue = "Normal";
    }
    if (input.val() == "1") {
      resultValue = "Important";
    }
  }
  if (input.attr('name') == 'publication_status') {
    if (input.val() == "0") {
      resultValue = "Published";
    }
    if (input.val() == "1") {
      resultValue = "Unpublished";
    }
  }
  // if (input.attr('name') == 'details_fake') {
  //   for (instance in CKEDITOR.instances) {
  //     ckresult = CKEDITOR.instances[instance].getData();
  //   }
  //   resultValue = "XXXXXXXXXX";
  // }

  return resultValue;
}

$("#termsConditions_input").click(function () {
  $("#termsConditions_error").addClass("hidden");
  $("#termsConditions_error").removeClass("border-danger-2");
});
// form.submit(function (event) {
  // event.preventDefault();
$("#submitBtn").click(function(){

  event.preventDefault();

  if ($("#termsConditions_input").is(":checked") == false) {

    $("#termsConditions_error").removeClass("hidden");
    $("#termsConditions_error").addClass("border-danger-2");

  }
  else {

    $("#termsConditions_error").addClass("hidden");
    $("#termsConditions_error").removeClass("border-danger-2");

    $('#modal-submit-confirmation').modal('toggle');

    var visibleFields = ['type', 'blood_group', 'blood_bag', 'organ_name', 'tissue_name', 'quantity', 'contact', 'contact2', 'contact3', 'contact_privacy', 'location', 'hospital', 'preferred_date', 'preferred_date_from', 'preferred_date_to', 'priority', 'publication_status'];

    var fail = false;
    var fail_log = '';
    var name;
    var input_group_id;
    var input_label;
    var confirm_log = '';
    var input_value;

    form.find('select, textarea, input').each(function () {
      // console.log($(this).attr('name'));
      input_group_id = $(this).attr('id') + "-group";
      input_label = $("#" + $(this).attr('name') + "-label").text();
      name = $(this).attr('name');
      input_value = $(this).val();

      function isVisibleField(value, arr) {
        var status = 0; // Not Exists
        for (var i = 0; i < arr.length; i++) {
          var name = arr[i];
          if (name == value) {
            status = 1; // Exists
            break;
          }
        }
        return status;
      }

      if (!$(this).prop('required')) {
        if (isVisibleField($(this).attr('name'), visibleFields) == 1) {
          if ($(this).val() != "") {
            confirm_log += input_label + ": <span class='text-info'>" + getValue($(this)) + "</span> \n <br>";
          }
        }
      } else {
        if ($("#" + input_group_id).hasClass("hidden") == false) {
          if (!$(this).val()) {
            fail = true;
            fail_log += "<span class='font-italic text-info'>" + input_label + "</span> is required! Please fill this field.\n <br>";
          }
          else {
            if (isVisibleField($(this).attr('name'), visibleFields) == 1) {
              if ($(this).val() != "") {
                confirm_log += input_label + ": <span class='text-info'>" + getValue($(this)) + "</span> \n <br>";
              }
            }
          }
        }
      }
    });
    if (!fail) {
      //process form here.
      $("#data_container").removeClass("hidden");
      $("#donation_form_errors_div").addClass("hidden");
      $("#data_container").html(confirm_log).css("color", "black");
      $("#cancelBtn").html("Cancel");
      $("#confirmDonationSubmit").removeClass("hidden");
    } else {
      // alert( fail_log );
      $("#donation_form_errors_div").removeClass("hidden");
      $("#data_container").addClass("hidden");
      $("#donation_form_errors").html(fail_log).css("color", "red");
      $("#cancelBtn").html("OK");
      $("#confirmDonationSubmit").addClass("hidden");
    }
  }
    
    
});

// final submission of form
$(document).ready(function(){
  $("#confirmDonationSubmit").click(function(){

    event.preventDefault();

    $('#modal-submit-confirmation').modal('hide');

    var serializedData = $(this).serialize();

    var loc = window.location;
    // var endpoint = wsStart + loc.host + loc.pathname;
    var endpoint = loc.pathname;
    // var endpoint = "/donations/offer/";

    if (type_input.val() == "Blood" && blood_group_input.val() == "") {
      event.preventDefault();
      $("#blood_group_msg").html("Please select blood group. It is required.");
    }
    else if (type_input.val() == "Blood" && blood_bag_input.val() == "") {
      if (page_title.val() != "Create donation offer" || page_title.val() != "Update donation offer") {
        event.preventDefault();
        $("#blood_bag_msg").html(
          "Please enter blood bag quantity. It is required."
        );
      }
    } else if (
      type_input.val() == "Organ" &&
      organ_name_input.val() == ""
    ) {
      event.preventDefault();
      $("#organ_name_msg").html("Please select organ name. It is required.");
    } else if (type_input.val() == "Tissue" && tissue_name_input.val() == "") {
      event.preventDefault();
      $("#tissue_name_msg").html(
        "Please select tissue name. It is required."
      );
    }
    else if (type_input.val() == "Organ" && quantity_input.val() == "") {
      event.preventDefault();
      $("#quantity_msg").html(
        "Please enter quantity. It is required."
      );
    }
     else if (
      contact_input.val() == "" ||
      contact_input.val().length != contact_input.attr("placeholder").length
    ) {
      event.preventDefault();
      $("#contact_msg").html("Please enter a valid contact number.");
    }
    else if ((contact2_input.val() != "") && (contact2_input.val().length != contact2_input.attr("placeholder").length)) {
     event.preventDefault();
     $("#contact2_msg").html("Please enter a valid contact number.");
   }
   else if ((contact3_input.val() != "") && (contact3_input.val().length != contact3_input.attr("placeholder").length)) {
    event.preventDefault();
    $("#contact3_msg").html("Please enter a valid contact number.");
  }
    else {
      if (blood_group_group.hasClass("hidden") == true) {
        blood_group_input.val("");
        blood_bag_input.val("");
      }
      if (page_title.val() != "Create donation offer" || page_title.val() != "Update donation offer") {
        if (blood_bag_group.hasClass("hidden") == true) {
          blood_bag_input.val("");
        }
      }
      if (organ_name_group.hasClass("hidden") == true) {
        organ_name_input.val("");
      }
      if (tissue_name_group.hasClass("hidden") == true) {
        tissue_name_input.val("");
      }
      if (quantity_group.hasClass("hidden") == true) {
        quantity_input.val("");
      }
      if (contact2_group.hasClass("hidden") == true) {
        contact2_input.val("");
      }
      if (contact3_group.hasClass("hidden") == true) {
        contact3_input.val("");
      }
      if (details_fake_group.hasClass("hidden") == true) {
        for (instance in CKEDITOR.instances) {
          CKEDITOR.instances[instance].setData(" ");
        }
      }
      if (details_group.hasClass("hidden") == true) {
        details_input.val("");
      }
      if (preferred_date_from_group.hasClass("hidden") == true) {
        preferred_date_from_input.val("");
      }
      if (preferred_date_to_group.hasClass("hidden") == true) {
        preferred_date_to_input.val("");
      }
      event.preventDefault();
      form.submit(); // Submit the form
      return true;
    }
  });
});

// Error handling
$(document).ready(function () {
  if (contact_input.val() != "" && contact2_input.val() == "") {
    add_second_contact.removeClass("hidden");
  } else {
    add_second_contact.addClass("hidden");
  }
  if (contact2_input.val() != "" && contact3_input.val() == "") {
    add_third_contact.removeClass("hidden");
  } else {
    add_third_contact.addClass("hidden");
  }

  if (type_input.val() != "" && type_input.val() == 0) {
    blood_group_group.removeClass("hidden");
    if (page_title.val() != "Create donation offer" || page_title.val() != "Update donation offer") {
        blood_bag_group.removeClass("hidden");
      }
  }

  if (type_input.val() != "" && type_input.val() == 1) {
    organ_name_group.removeClass("hidden");
  }
  else{
    organ_name_group.addClass("hidden");
  }

  if (type_input.val() != "" && type_input.val() == 2) {
    tissue_name_group.removeClass("hidden");
  } else {
    tissue_name_group.addClass("hidden");
  }

  // if (details_fake_input.val() != "") {
  //   details_group.addClass("hidden");
  //   advanced_editing.addClass("hidden");
  //   details_fake_group.removeClass("hidden");
  //   basic_editing.removeClass("hidden");
  // }

  $("#offer_create_form input").each(function () {
    var $this = $(this);
    var id = $this.attr("id");
    if ($this.val() != "") {
      $("#" + id + "-group").removeClass("hidden");
      if ($this.hasClass("special-input")) {
        special_input_group.removeClass("hidden");
        advanced.addClass("hidden");
        hide_advanced.removeClass("hidden");
      }
    }
  });
  $.each(form_error, function () {
    var $this = $(this);
    var error_input_id = $this.attr("id").replace("_error", "");
    // if ($("#donation_" + error_input_id + "_input").hasClass("special-input")) {
    //   special_input_group.removeClass("hidden");
    // }
    if (
      error_input_id == "preferred_date_from" ||
      error_input_id == "preferred_date_to"
    ) {
      set_date_between.addClass("hidden");
    }
    // $("#donation_" + error_input_id + "-group").removeClass("hidden");
    $("#donation_" + error_input_id + "_input").focus();
  });
  // if (form_error.hasClass("special-input")) {
  //   alert("XXX");
  //   form_error.closest("div.special-input-group").removeClass("hidden");
  // }
});

// $(document).ready(function() {
//   if ((contact_input.val() != "") && (contact2_input.val() == "")) {
//     add_second_contact.removeClass("hidden");
//   } else {
//     add_second_contact.addClass("hidden");
//   }
//   if ((contact2_input.val() != "") && (contact3_input.val() == "")) {
//     add_third_contact.removeClass("hidden");
//   } else {
//     add_third_contact.addClass("hidden");
//   }
// });

// $(contact_input).keyup(function() {
//   $this = $(this);
//   var test = $this.intlTelInput("getSelectedCountryData").dialCode;
//   console.log(test);
// });

// console.log(page_title.val());
$(document).ready(function () {
  if ((page_title.val() == "Create donation offer") || page_title.val() == "Update donation offer") {
    // console.log("true");
    $("#donation_blood_group_input option[value='Any Blood Group']").each(function () {
      $(this).remove();
    });
    $("#donation_title_input").attr("placeholder", "I want to donate ...");
    $("#donation_priority_input-group").addClass("hidden");
    // console.log($("#can_donate_blood").val());
    // console.log(JSON.stringify($("#can_donate_blood").val()).toLowerCase());
    if (JSON.stringify($("#can_donate_blood").val()).toLowerCase() == JSON.stringify("false")) {
      // console.log("Worked!");
      $("#blood_warning_simple").removeClass("hidden");
      $("#donation_type_input option[value=0]").each(function () {
        $(this).remove();
      });
    }
  };
});

// preventing form from autocomplete
$(document).ready(function () {
  $(document).on("focus", ":input", function () {
    $(this).attr("autocomplete", "off");
  });
});

// Map Detect User Current Location
(function ($, google) {
  js_location_detect.on("click", function (e) {
    // location_fake_input.geolocate({
    //   loading: "detecting....",
    //   formatted_address: true,
    //   // components: [
    //   //   // "street_address",
    //   //   // "street_number",
    //   //   "locality",
    //   //   "administrative_area_level_1",
    //   //   "postal_code",
    //   //   // "political",
    //   //   "country"
    //   // ],
    //   name: "long_name", // "short_name", "long_name"
    //   delimeter: ", ",
    //   enableHighAccuracy: true,
    //   timeout: 5000,
    //   maximumAge: 0
    // });
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
