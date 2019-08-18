var form = $("#donationBank_donation_manage_form");
var form_error = $(".form-error");
var step_fields = ['first_name', 'last_name', 'email', 'gender', 'dob', 'diseases', 'contact', 'address', 'city', 'state', 'country', 'donation_type', 'blood_group', 'organ_name', 'tissue_name', 'quantity', 'collection_date', 'expiration_date', 'description']

var step_field_0 = ['first_name', 'last_name', 'email', 'gender', 'dob', 'diseases']
var step_field_1 = ['contact', 'address', 'city', 'state', 'country']
var step_field_2 = ['donation_type', 'blood_group', 'organ_name', 'tissue_name', 'quantity', 'collection_date', 'expiration_date', 'description']

var dob_input = $("#donation_dob_input");
var dob_group = $("#donation_dob_input-group");


function isInStepFields(value, arr) {
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

$.each(form_error, function () {
    var $this = $(this);
    // console.log($this);
    var error_input_id = $this.attr("id").replace("_error", "");
    // $("#donation_" + error_input_id + "-group").removeClass("hidden");
    var input = $("#donation_" + error_input_id + "_input");
    input.focus();
    input_name = input.attr('name');
    if (isInStepFields(input_name, step_field_2) == 1) {
        $("#startIndex").val(2)
    } else if (isInStepFields(input_name, step_field_1) == 1) {
        $("#startIndex").val(1)
    } else {
        $("#startIndex").val(0)
    }
});

// Dynamic Start Index of Jquery Steps based on Error reports
var startIndex_dynamic;
var startIndex_dynamic = Number($("#startIndex").val());

// Error Handling
$(document).ready(function () {
    $("#donation_quantity_input-group").addClass("hidden");
    $("#donation_quantity_input").attr("required", false);
    $('form:first *:input[type!=hidden]:first').focus();

    // remove hidden if input has value (Required in Update View)
    $("#donationBank_donation_manage_form input").each(function () {
        var $this = $(this);
        var id = $this.attr("id");
        if ($this.val() != "") {
            $("#" + id + "-group").removeClass("hidden");
        }
    });
});


// form.validate({
//     errorPlacement: function errorPlacement(error, element) { element.before(error); },
//     rules: {
//         confirm: {
//             equalTo: "#password"
//         }
//     }
// });
$("#wizard").steps({
    headerTag: "h4",
    bodyTag: "fieldset",
    transitionEffect: "slideLeft",
    // enableAllSteps: true,
    // enablePagination: false,
    // suppressPaginationOnFocus: true,
    // enableCancelButton: false,
    // enableFinishButton: true,
    // saveState: false,
    startIndex: startIndex_dynamic,
    onStepChanging: function (event, currentIndex, newIndex) {
        // Allways allow previous action even if the current form is not valid!
        if (currentIndex > newIndex) {
            return true;
        }
        // Forbid next action on "Warning" step if the user is to young
        // if (newIndex === 3 && Number($("#age-2").val()) < 18) {
        //     return false;
        // }
        // Needed in some cases if the user went back (clean up)
        if (currentIndex < newIndex) {
            // To remove error styles
            form.find(".body:eq(" + newIndex + ") label.error").remove();
            form.find(".body:eq(" + newIndex + ") .error").removeClass("error");
        }
        form.validate().settings.ignore = ":disabled,:hidden";
        return form.valid();
    },
    onStepChanged: function (event, currentIndex, priorIndex) {
        // Used to skip the "Warning" step if the user is old enough.
        // if (currentIndex === 2 && Number($("#age-2").val()) >= 18) {
        //     form.steps("next");
        // }
        // Used to skip the "Warning" step if the user is old enough and wants to the previous step.
        if (currentIndex === 2 && priorIndex === 3) {
            form.steps("previous");
        }
    },
    onFinishing: function (event, currentIndex) {
        form.validate().settings.ignore = ":disabled";
        return form.valid();
    },
    onFinished: function (event, currentIndex) {
        // alert("Submitted!");
        form.submit();
        // return true;
    }
}).validate({
    errorPlacement: function errorPlacement(error, element) {
        element.before(error);
    }
    // },
    // rules: {
    //     confirm: {
    //         equalTo: "#password-2"
    //     }
    // }
});

function resetMessage() {
    $(".input-message").html("");
    $(".form-error-div").html("");
    $(".form-group").removeClass("border-danger-1");
}


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

    $("#donation_dob_input").datetimepicker({
        timepicker: false,
        format: "Y-m-d",
        maxDate: now(),
        validateOnBlur: true,
        // onChangeDateTime:function(dp,$input){
        //   alert($input.val());
        //   dob = new Date($input.val());
        //   var today = new Date();
        //   console.log(dob);
        //   console.log(dob_input.val());
        //   var age = Math.floor((today - dob) / (365.25 * 24 * 60 * 60 * 1000));
        //   console.log(age);
        // },
    });
    
    $("#donation_collection_date_input").datetimepicker({
        timepicker: false,
        format: "Y-m-d",
        maxDate: now(),
        validateOnBlur: true
    });
    $("#donation_expiration_date_input").datetimepicker({
        timepicker: false,
        format: "Y-m-d",
        // maxDate: now(),
        minDate: now(),
        validateOnBlur: true
    });
});

// preventing form from autocomplete
$(document).ready(function () {
    $(document).on("focus", ":input", function () {
        $(this).attr("autocomplete", "off");
    });
});

// Other Form JS Works

var contactPattern = new RegExp("^(\\+)?(\\d+)$");

function chkInput() {
    var v = $("#donation_contact_input").val().charAt($("#donation_contact_input").val().length - 1);
    return contactPattern.test(v);
}

$("#donation_contact_input").on('keyup keypress blur change input keydown mousedown mouseup select contextmenu drop', function () {
    if ($(this).val().length == 1 || ($(this).val().length == 2 && $("#donation_contact_input").val().charAt($("#donation_contact_input").val().length - 1) == "0")) $(this).val('+');
    else {
        var res = chkInput();
        if (!res) $(this).val($(this).val().slice(0, -1));
    }
});



// --- type select function ---
function donationTypeFunction() {
    resetMessage();
    if ($("#donation_donation_type_input").val() == 0) {
        $("#donation_tissue_name_input-group").addClass("hidden");
        $("#donation_organ_name_input-group").addClass("hidden");
        $("#donation_organ_name_input").attr("required", false);
        $("#donation_tissue_name_input").attr("required", false);
        $("#donation_quantity_input-group").removeClass("hidden");
        $("#donation_quantity_input").attr("required", true);
        $("#quantity_priority").html("(required)");
        $("#quantity_priority").addClass("text-info");
        $("#donation_quantity_input").val(1);
        $("#donation_tissue_name_input").val("");
        $("#donation_organ_name_input").val("");
        // console.log($("#donation_donation_type_input").val());
    } else if ($("#donation_donation_type_input").val() == 1) {
        $("#donation_tissue_name_input-group").addClass("hidden");
        $("#donation_organ_name_input-group").removeClass("hidden");
        $("#organ_name_priority").html("(required)");
        $("#organ_name_priority").addClass("text-info");
        $("#donation_organ_name_input").attr("required", true);
        $("#donation_tissue_name_input").attr("required", false);
        $("#donation_quantity_input-group").removeClass("hidden");
        $("#donation_quantity_input").attr("required", true);
        $("#quantity_priority").html("(required)");
        $("#quantity_priority").addClass("text-info");
        $("#donation_quantity_input").val(1);
        $("#donation_tissue_name_input").val("");
        // console.log($("#donation_donation_type_input").val());
    } else if ($("#donation_donation_type_input").val() == 2) {
        $("#donation_tissue_name_input-group").removeClass("hidden");
        $("#tissue_name_priority").html("(required)");
        $("#tissue_name_priority").addClass("text-info");
        $("#donation_organ_name_input").attr("required", false);
        $("#donation_tissue_name_input").attr("required", true);
        $("#donation_organ_name_input-group").addClass("hidden");
        $("#donation_quantity_input-group").addClass("hidden");
        $("#donation_quantity_input").attr("required", false);
        $("#donation_quantity_input").val("");
        $("#donation_organ_name_input").val("");
        // console.log($("#donation_donation_type_input").val());
    } else {
        $("#donation_tissue_name_input-group").addClass("hidden");
        $("#donation_organ_name_input-group").addClass("hidden");
        $("#donation_blood_group_input-group").addClass("hidden");
        $("#donation_quantity_input-group").addClass("hidden");
        $("#donation_quantity_input").val("");
        $("#donation_tissue_name_input").val("");
        $("#donation_organ_name_input").val("");
        $("#donation_blood_group_input").val("");
    }
}



function organFunction() {
    resetMessage();
    // Deceased Donations
    if ($("#donation_organ_name_input").val() == "Heart") {
        $("#donation_quantity_input").val(1);
        $("#donation_quantity_input").attr("disabled", true);
    } else if ($("#donation_organ_name_input").val() == "Liver") {
        $("#donation_quantity_input").val(1);
        $("#donation_quantity_input").attr("disabled", true);
    } else if ($("#donation_organ_name_input").val() == "Pancreas") {
        $("#donation_quantity_input").val(1);
        $("#donation_quantity_input").attr("disabled", true);
    } else if ($("#donation_organ_name_input").val() == "Intestines") {
        $("#donation_quantity_input").val(1);
        $("#donation_quantity_input").attr("disabled", true);
    }
    // Living Donations
    else if ($("#donation_organ_name_input").val() == "Lungs") {
        $("#donation_quantity_input").val(1);
        $("#donation_quantity_input").attr("disabled", false);
    } else if ($("#donation_organ_name_input").val() == "Kidney") {
        $("#donation_quantity_input").val(1);
        $("#donation_quantity_input").attr("disabled", false);
    } else {
        $("#donation_quantity_input").attr("disabled", false);
    }
}



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

$("#donation_quantity_input").inputFilter(function (value) {
    return /^\d*$/.test(value) && (value === "" || parseInt(value) <= 2);
});