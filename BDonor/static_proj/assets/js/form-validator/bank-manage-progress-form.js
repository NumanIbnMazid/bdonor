var form = $("#donation_progress_form");
var submitBtn = $("#submitBtn");
var progress_status_input = $("#donation_progress_status_input");
var progress_status_group = $("#donation_progress_status_input-group");
var completion_date_input = $("#donation_progress_completion_date_input");
var completion_date_group = $("#donation_progress_completion_date_input-group");
var first_name_input = $("#donation_progress_first_name_input");
var first_name_group = $("#donation_progress_first_name_input-group");
var last_name_input = $("#donation_progress_last_name_input");
var last_name_group = $("#donation_progress_last_name_input-group");
var gender_input = $("#donation_progress_gender_input");
var gender_group = $("#donation_progress_gender_input-group");
var blood_group_input = $("#donation_progress_blood_group_input");
var blood_group_group = $("#donation_progress_blood_group_input-group");
var dob_input = $("#donation_progress_dob_input");
var dob_group = $("#donation_progress_dob_input-group");
var contact_input = $("#donation_progress_contact_input");
var contact_group = $("#donation_progress_contact_input-group");
var email_input = $("#donation_progress_email_input");
var email_group = $("#donation_progress_email_input-group");
var address_input = $("#donation_progress_address_input");
var address_group = $("#donation_progress_address_input-group");
var city_input = $("#donation_progress_city_input");
var city_group = $("#donation_progress_city_input-group");
var state_input = $("#donation_progress_state_input");
var state_group = $("#donation_progress_state_input-group");
var country_input = $("#donation_progress_country_input");
var country_group = $("#donation_progress_country_input-group");
var details_input = $("#donation_progress_details_input");
var details_group = $("#donation_progress_details_input-group");

var InputArray = new Array(progress_status_input, completion_date_input, first_name_input, last_name_input, gender_input, blood_group_input, dob_input, contact_input, email_input, address_input, city_input, state_input, country_input, details_input);
var InputGroup = new Array(progress_status_group, completion_date_group, first_name_group, last_name_group, gender_group, blood_group_group, dob_group, contact_group, email_group, address_group, city_group, state_group, country_group, details_group);

var correspondentInputArray = new Array(completion_date_input, first_name_input, last_name_input, gender_input, blood_group_input, dob_input, contact_input, email_input, address_input, city_input, state_input, country_input, details_input);
var correspondentInputGroup = new Array(completion_date_group, first_name_group, last_name_group, gender_group, blood_group_group, dob_group, contact_group, email_group, address_group, city_group, state_group, country_group, details_group);


function resetMessage() {
    $(".input-message").html("");
    $(".form-error-div").html("");
    $(".form-group").removeClass("border-danger-1");
}

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

    $("#donation_progress_completion_date_input").datetimepicker({
        timepicker: false,
        format: "Y-m-d",
        maxDate: now(),
        validateOnBlur: true
    });
    $("#donation_progress_dob_input").datetimepicker({
        timepicker: false,
        format: "Y-m-d",
        maxDate: now(),
        validateOnBlur: true
    });
});

// Contact Input
var contactPattern = new RegExp("^(\\+)?(\\d+)$");

function chkInput() {
    var v = $("#donation_progress_contact_input").val().charAt($("#donation_progress_contact_input").val().length - 1);
    return contactPattern.test(v);
}
$("#donation_progress_contact_input").on('keyup keypress blur change input keydown mousedown mouseup select contextmenu drop', function () {
    if ($(this).val().length == 1 || ($(this).val().length == 2 && $("#donation_progress_contact_input").val().charAt($("#donation_progress_contact_input").val().length - 1) == "0")) $(this).val('+');
    else {
        var res = chkInput();
        if (!res) $(this).val($(this).val().slice(0, -1));
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