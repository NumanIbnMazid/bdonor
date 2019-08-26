var form = $("#donationBank_campaign_manage_form");
var form_error = $(".form-error");
var title_input = $("#campaign_title_input");
var title_group = $("#campaign_title_input-group");
var contact_input = $("#campaign_contact_input");
var contact_group = $("#campaign_contact_input-group");
var held_date_input = $("#campaign_held_date_input");
var held_date_group = $("#campaign_held_date_input-group");
var end_date_input = $("#campaign_end_date_input");
var end_date_group = $("#campaign_end_date_input-group");

// preventing form from autocomplete
$(document).ready(function () {
    $(document).on("focus", ":input", function () {
        $(this).attr("autocomplete", "off");
    });
});

$.each(form_error, function () {
    var $this = $(this);
    $(".error-group").removeClass("hidden");
    var error_input_id = $this.attr("id").replace("_error", "");
    var input = $("#campaign_" + error_input_id + "_input");
    input.focus();
});

function resetMessage() {
    $(".input-message").html("");
    $(".form-error-div").html("");
    $(".form-group").removeClass("border-danger-1");
}

// Contact Input
var contactPattern = new RegExp("^(\\+)?(\\d+)$");
function chkInput() {
    var v = $("#campaign_contact_input").val().charAt($("#campaign_contact_input").val().length - 1);
    return contactPattern.test(v);
}
$("#campaign_contact_input").on('keyup keypress blur change input keydown mousedown mouseup select contextmenu drop', function () {
    if ($(this).val().length == 1 || ($(this).val().length == 2 && $("#campaign_contact_input").val().charAt($("#campaign_contact_input").val().length - 1) == "0")) $(this).val('+');
    else {
        var res = chkInput();
        if (!res) $(this).val($(this).val().slice(0, -1));
    }
});

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

    held_date_input.datetimepicker({
        onShow: function (ct) {
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
        },
        minDate: now(),
        validateOnBlur: true
    });

    end_date_input.datetimepicker({
        onShow: function (ct) {
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
        },
        minDate: now(),
        validateOnBlur: true
    });
});

