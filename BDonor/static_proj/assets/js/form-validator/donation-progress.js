var form = $("#donation_progress_form");
var submitBtn = $("#submitBtn");
var progress_status_input = $("#donation_progress_status_input");
var progress_status_group = $("#donation_progress_status_input-group");
var respondent_input = $("#donation_respondent_input");
var respondent_group = $("#donation_respondent_input-group");
var completion_date_input = $("#donation_completion_date_input");
var completion_date_group = $("#donation_completion_date_input-group");
var management_status_input = $("#donation_management_status_input");
var management_status_group = $("#donation_management_status_input-group");
var details_input = $("#donation_details_input");
var details_group = $("#donation_details_input-group");

var InputArray = new Array(progress_status_input, respondent_input, completion_date_input, management_status_input, details_input);
var InputGroup = new Array(progress_status_group, respondent_group, completion_date_group, management_status_group, details_group);

var correspondentInputArray = new Array(respondent_input, completion_date_input, management_status_input, details_input);
var correspondentInputGroup = new Array(respondent_group, completion_date_group, management_status_group, details_group);


$(document).ready(function () {
  if (progress_status_input.val() == 0) {
    // for (var i = 0; i < correspondentInputArray.length; i++) {
    //   $(correspondentInputArray[i]).val("");
    // }
    for (var i = 0; i < correspondentInputGroup.length; i++) {
      $(correspondentInputGroup[i]).addClass("hidden");
    }
  } else {
    // for (var i = 0; i < correspondentInputArray.length; i++) {
    //   $(correspondentInputArray[i]).val("");
    // }
    for (var i = 0; i < correspondentInputGroup.length; i++) {
      $(correspondentInputGroup[i]).removeClass("hidden");
    }
  }
});

$("#donation_progress_status_input").change(function (el) {
  if (($(el.target).val()) == 0) {
    // for (var i = 0; i < correspondentInputArray.length; i++) {
    //   $(correspondentInputArray[i]).val("");
    // }
    for (var i = 0; i < correspondentInputGroup.length; i++) {
      $(correspondentInputGroup[i]).addClass("hidden");
    }
  } else {
    // for (var i = 0; i < correspondentInputArray.length; i++) {
    //   $(correspondentInputArray[i]).val("");
    // }
    for (var i = 0; i < correspondentInputGroup.length; i++) {
      $(correspondentInputGroup[i]).removeClass("hidden");
    }
  }
});

//$(document).on('change', $("#donation_progress_status_input"), function(el) {
//    console.log($(el.target).val());
//});

// date-time picker
$(document).ready(function () {
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

  $("#donation_completion_date_input").datetimepicker({
    timepicker: false,
    format: "Y-m-d",
    maxDate: now(),
    validateOnBlur: true
  });
});

$(document).ready(function () {
  if ($("#respondent_count").val() < 1) {
    $("#respondent_extra_info").text("No Respondent Found !!!").addClass("text-danger text-center font-bold font-15 m-2");
    $("#donation_respondent_input").addClass("hidden");
  }
  else{
    $("#respondent_extra_info").text();
    $("#donation_respondent_input").removeClass("hidden");
    $("#respondent_help_block").text("Hold down 'Control', or 'Command' on a Mac, to select more than one");
  }
});


submitBtn.click(function () {
  event.preventDefault();
  if (progress_status_input.val() == 0) {
    for (var i = 0; i < correspondentInputArray.length; i++) {
      //console.log($(correspondentInputArray[i]).val());
      $(correspondentInputArray[i]).val("");
    }
  }
  form.submit();
  return true;
});

// preventing form from autocomplete
$(document).ready(function () {
  $(document).on("focus", ":input", function () {
    $(this).attr("autocomplete", "off");
  });
});