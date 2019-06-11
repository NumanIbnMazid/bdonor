// ===================== Donation Form JS ======================
var form = $("#offer_create_form");
var submitBtn = $("#submitBtn");
var message_holder = $("#message_holder");
var advanced = $("#advanced");
var hide_advanced = $("#hide_advanced");
var type_input = $("#donation_type_input");
var custom_type_input = $("#donation_custom_type_input");
var custom_type_group = $("#donation_custom_type_input-group");
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

// Check if string is HTML or Not
function isHTML(str) {
  var a = document.createElement("div");
  a.innerHTML = str;

  for (var c = a.childNodes, i = c.length; i--; ) {
    if (c[i].nodeType == 1) return true;
  }

  return false;
}

// console.log(moment().format('MMMM Do YYYY, h:mm:ss a'));

// Map Detect User Current Location
(function($, google) {
  detect_location.on("click", function(e) {
    location_input.geolocate({
      loading: "detecting....",
      formatted_address: true,
      components: [
        // "street_address",
        // "street_number",
        "locality",
        "administrative_area_level_1",
        "postal_code",
        // "political",
        "country"
      ],
      name: "long_name", // "short_name", "long_name"
      delimeter: ", ",
      enableHighAccuracy: true,
      timeout: 5000,
      maximumAge: 0
    });
  });
})(jQuery, google);

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
contact2_input.inputFilter(function(value) {
  return /^\d*$/.test(value);
});
contact3_input.inputFilter(function(value) {
  return /^\d*$/.test(value);
});
// blood_bag_input.inputFilter(function(value) {
//   return /^\d*$/.test(value);
// });

// ends force to enter only number 0-9

// force to enter only number between 100
blood_bag_input.inputFilter(function(value) {
  return /^\d*$/.test(value) && (value === "" || parseInt(value) <= 100);
});
// ends force to enter only number between 100

// force to match the minimum and maximum length

contact_input.keypress(function(e) {
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

contact2_input.keypress(function(e) {
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

contact3_input.keypress(function(e) {
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
$(document).ready(function() {
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
    } 
    else {
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
  advanced_editing.click(function() {
    // details_input.val("");
    details_fake_group.removeClass("hidden");
    details_group.addClass("hidden");
    advanced_editing.addClass("hidden");
    basic_editing.removeClass("hidden");
  });
  basic_editing.click(function() {
    // details_fake_input.val("");
    // for (instance in CKEDITOR.instances) {
    //   CKEDITOR.instances[instance].setData(" ");
    // }
    details_fake_group.addClass("hidden");
    details_group.removeClass("hidden");
    advanced_editing.removeClass("hidden");
    basic_editing.addClass("hidden");
  });
  advanced.click(function() {
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
  });
  hide_advanced.click(function() {
    special_input_group.addClass("hidden");
    advanced.removeClass("hidden");
    if (set_date_between.hasClass("hidden")) {
      preferred_date_from_group.addClass("hidden");
      preferred_date_to_group.addClass("hidden");
    }
    hide_advanced.addClass("hidden");
  });
  hide_contact2.click(function() {
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
  hide_contact3.click(function() {
    contact3_group.addClass("hidden");
    contact3_input.val("");
    if (
      contact2_input.val().length == contact_input.attr("placeholder").length
    ) {
      add_third_contact.removeClass("hidden");
    }
  });
  add_second_contact.click(function() {
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
  set_date_between.click(function() {
    preferred_date_from_group.removeClass("hidden");
    preferred_date_to_group.removeClass("hidden");
    set_date_between.addClass("hidden");
    hide_set_date_between.removeClass("hidden");
  });
  hide_set_date_between.click(function() {
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
  date_with_time.click(function() {
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
  date_without_time.click(function() {
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

function resetMessage() {
  $(".input-message").html("");
}

// =========== intlTelInput Phone =============

// contact 1
contact_input[0].addEventListener("open:countrydropdown", function() {
  contact_input.attr("maxlength", 15);
  contact_input.attr("minlength", 15);
});

contact_input[0].addEventListener("close:countrydropdown", function() {
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
contact2_input[0].addEventListener("open:countrydropdown", function() {
  contact2_input.attr("maxlength", 15);
  contact2_input.attr("minlength", 15);
});

contact2_input[0].addEventListener("close:countrydropdown", function() {
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
contact3_input[0].addEventListener("open:countrydropdown", function() {
  contact3_input.attr("maxlength", 15);
  contact3_input.attr("minlength", 15);
});

contact3_input[0].addEventListener("close:countrydropdown", function() {
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
    custom_type_group.addClass("hidden");
    organ_name_group.addClass("hidden");
    blood_group_group.removeClass("hidden");
    blood_bag_group.removeClass("hidden");
    $("#blood_group_priority").html("(required)");
    $("#blood_group_priority").addClass("text-info");
    blood_group_input.attr("required", true);
    $("#blood_bag_priority").html("(required)");
    $("#blood_bag_priority").addClass("text-info");
    blood_bag_input.attr("required", true);
    organ_name_input.attr("required", false);
    custom_type_input.attr("required", false);
    custom_type_input.val("");
    organ_name_input.val("");
  } else if (type_input.val() == 1) {
    custom_type_group.addClass("hidden");
    organ_name_group.removeClass("hidden");
    $("#organ_name_priority").html("(required)");
    $("#organ_name_priority").addClass("text-info");
    blood_group_input.attr("required", false);
    blood_bag_input.attr("required", false);
    organ_name_input.attr("required", true);
    custom_type_input.attr("required", false);
    blood_group_group.addClass("hidden");
    blood_bag_group.addClass("hidden");
    custom_type_input.val("");
    blood_group_input.val("");
    blood_bag_input.val("");
  } else if (type_input.val() == 2) {
    custom_type_group.removeClass("hidden");
    $("#custom_type_priority").html("(required)");
    $("#custom_type_priority").addClass("text-info");
    blood_group_input.attr("required", false);
    blood_bag_input.attr("required", false);
    organ_name_input.attr("required", false);
    custom_type_input.attr("required", true);
    organ_name_group.addClass("hidden");
    blood_group_group.addClass("hidden");
    blood_bag_group.addClass("hidden");
    organ_name_input.val("");
    blood_group_input.val("");
    blood_bag_input.val("");
  } else {
    custom_type_group.addClass("hidden");
    organ_name_group.addClass("hidden");
    blood_group_group.addClass("hidden");
    blood_bag_group.addClass("hidden");
    custom_type_input.val("");
    organ_name_input.val("");
    blood_group_input.val("");
    blood_bag_input.val("");
  }
}

$(contact_input).keyup(function() {
  resetMessage();
  var $this = $(this);
  var contactValue = $this.val();
  if (contactValue.length == contact_input.attr("placeholder").length) {
    if (contact2_group.hasClass("hidden") == true) {
      add_second_contact.removeClass("hidden");
    }
    add_second_contact.click(function() {
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

$(contact2_input).keyup(function() {
  resetMessage();
  var $this = $(this);
  var contact2Value = $this.val();
  if (contact2Value.length == contact2_input.attr("placeholder").length) {
    if (contact3_group.hasClass("hidden") == true) {
      add_third_contact.removeClass("hidden");
    }
    add_third_contact.click(function() {
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

// date-time picker
$(document).ready(function() {
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
    onShow: function(ct) {
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
    onShow: function(ct) {
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
    onShow: function(ct) {
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

form.submit(function(event) {
  // event.preventDefault();

  var serializedData = $(this).serialize();

  var loc = window.location;
  // var endpoint = wsStart + loc.host + loc.pathname;
  var endpoint = loc.pathname;
  // var endpoint = "/donations/offer/";

  if (type_input.val() == "Blood" && blood_group_input.val() == "") {
    event.preventDefault();
    $("#blood_group_msg").html("Please select blood group. It is required.");
  } else if (type_input.val() == "Blood" && blood_bag_input.val() == "") {
    event.preventDefault();
    $("#blood_bag_msg").html(
      "Please enter blood bag quantity. It is required."
    );
  } else if (
    type_input.val() == "Body Organs" &&
    organ_name_input.val() == ""
  ) {
    event.preventDefault();
    $("#organ_name_msg").html("Please type organ name. It is required.");
  } else if (type_input.val() == "Others" && custom_type_input.val() == "") {
    event.preventDefault();
    $("#custom_type_msg").html(
      "Please type donation type name. It is required."
    );
  } else if (
    contact_input.val() == "" ||
    contact_input.val().length != contact_input.attr("placeholder").length
  ) {
    event.preventDefault();
    $("#contact_msg").html("Please enter a valid contact number.");
  } else {
    // console.log("XXXXX");
    // if (details_fake_input.val() != "") {
    //   details_input.val(details_fake_input.val());
    // }
    // if (contact_input.val() != "") {
    //   contact_input.val(contactFake.val()+contact_input.val());
    // }
    // if (contact2_input.val() != "") {
    //   contact2_input.val(contact2Fake.val()+contact2_input.val());
    // }
    // if (contact3_input.val() != "") {
    //   contact3_input.val(contact3Fake.val()+contact3_input.val());
    // }
    if (blood_group_group.hasClass("hidden") == true) {
      blood_group_input.val("");
    }
    if (blood_bag_group.hasClass("hidden") == true) {
      blood_bag_input.val("");
    }
    if (organ_name_group.hasClass("hidden") == true) {
      organ_name_input.val("");
    }
    if (custom_type_group.hasClass("hidden") == true) {
      custom_type_input.val("");
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
    return true;
  }
});

// Error handling
$(document).ready(function() {
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
    blood_bag_group.removeClass("hidden");
  }

  // if (details_fake_input.val() != "") {
  //   details_group.addClass("hidden");
  //   advanced_editing.addClass("hidden");
  //   details_fake_group.removeClass("hidden");
  //   basic_editing.removeClass("hidden");
  // }

  $("#offer_create_form input").each(function() {
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
  $.each(form_error, function() {
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

// preventing form from autocomplete
$(document).ready(function() {
  $(document).on("focus", ":input", function() {
    $(this).attr("autocomplete", "off");
  });
});
