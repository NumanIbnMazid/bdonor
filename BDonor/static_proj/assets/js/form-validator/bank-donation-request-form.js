// Variable Declaration
var form = $("#donationBank_donation_request_manage_form");
var submitBtn = $("#submitBtn");
var type_input = $("#donation_request_donation_type_input");
var type_input_group = $("#donation_request_donation_type_input-group");
var blood_group_input = $("#donation_request_blood_group_input");
var blood_group_group = $("#donation_request_blood_group_input-group");
var organ_name_input = $("#donation_request_organ_name_input");
var organ_name_group = $("#donation_request_organ_name_input-group");
var tissue_name_input = $("#donation_request_tissue_name_input");
var tissue_name_group = $("#donation_request_tissue_name_input-group");
var quantity_input = $("#donation_request_quantity_input");
var quantity_group = $("#donation_request_quantity_input-group");
var details_input = $("#donation_request_details_input");
var details_group = $("#donation_request_details_input-group");
var field_priority = $(".field_priority");
var form_error = $(".form-error");
var error_group = $(".error-group");

// Functions

function resetMessage() {
    $(".input-message").html("");
    $(".form-error-div").html("");
    $(".form-group").removeClass("border-danger-1");
}

// Check if string is HTML or Not
// function isHTML(str) {
//     var a = document.createElement("div");
//     a.innerHTML = str;

//     for (var c = a.childNodes, i = c.length; i--;) {
//         if (c[i].nodeType == 1) return true;
//     }

//     return false;
// }

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

quantity_input.inputFilter(function (value) {
    return /^\d*$/.test(value) && (value === "" || parseInt(value) <= 100);
});


// Error Handling
$(document).ready(function () {
    $('form:first *:input[type!=hidden]:first').focus();
    $(".error-group").removeClass("hidden");
    // remove hidden if input has value (Required in Update View)
    $("form input, form select, form textarea").each(function () {
        var $this = $(this);
        var id = $this.attr("id");
        // console.log(id);
        if ($this.val() != "") {
            $("#" + id + "-group").removeClass("hidden");
        }
    });
});

// preventing form from autocomplete
$(document).ready(function () {
    $(document).on("focus", ":input", function () {
        $(this).attr("autocomplete", "off");
    });
});



// --- type select function ---
function donationTypeFunction() {
    resetMessage();
    if ($("#donation_request_donation_type_input").val() == 0) {
        $("#donation_request_tissue_name_input-group").addClass("hidden");
        $("#donation_request_organ_name_input-group").addClass("hidden");
        $("#donation_request_organ_name_input").attr("required", false);
        $("#donation_request_tissue_name_input").attr("required", false);
        $("#donation_request_quantity_input-group").removeClass("hidden");
        $("#donation_request_quantity_input").attr("required", true);
        $("#quantity_priority").html("(required)");
        $("#quantity_priority").addClass("text-info");
        $("#donation_request_quantity_input").val(1);
        // $("#donation_request_quantity_input").attr("disabled", true);
        $("#donation_request_tissue_name_input").val("");
        $("#donation_request_organ_name_input").val("");
        // console.log($("#donation_request_donation_type_input").val());
    } else if ($("#donation_request_donation_type_input").val() == 1) {
        $("#donation_request_tissue_name_input-group").addClass("hidden");
        $("#donation_request_organ_name_input-group").removeClass("hidden");
        $("#organ_name_priority").html("(required)");
        $("#organ_name_priority").addClass("text-info");
        $("#donation_request_organ_name_input").attr("required", true);
        $("#donation_request_tissue_name_input").attr("required", false);
        $("#donation_request_quantity_input-group").removeClass("hidden");
        $("#donation_request_quantity_input").attr("required", true);
        $("#quantity_priority").html("(required)");
        $("#quantity_priority").addClass("text-info");
        $("#donation_request_quantity_input").val(1);
        $("#donation_request_tissue_name_input").val("");
        // console.log($("#donation_request_donation_type_input").val());
    } else if ($("#donation_request_donation_type_input").val() == 2) {
        $("#donation_request_tissue_name_input-group").removeClass("hidden");
        $("#tissue_name_priority").html("(required)");
        $("#tissue_name_priority").addClass("text-info");
        $("#donation_request_organ_name_input").attr("required", false);
        $("#donation_request_tissue_name_input").attr("required", true);
        $("#donation_request_organ_name_input-group").addClass("hidden");
        $("#donation_request_quantity_input-group").addClass("hidden");
        $("#donation_request_quantity_input").attr("required", false);
        $("#donation_request_quantity_input").val("");
        $("#donation_request_organ_name_input").val("");
        // console.log($("#donation_request_donation_type_input").val());
    } else {
        $("#donation_request_tissue_name_input-group").addClass("hidden");
        $("#donation_request_organ_name_input-group").addClass("hidden");
        $("#donation_request_blood_group_input-group").addClass("hidden");
        $("#donation_request_quantity_input-group").addClass("hidden");
        $("#donation_request_quantity_input").val("");
        $("#donation_request_tissue_name_input").val("");
        $("#donation_request_organ_name_input").val("");
        $("#donation_request_blood_group_input").val("");
    }
}



function organFunction() {
    resetMessage();
    // Deceased Donations
    if ($("#donation_request_organ_name_input").val() == "Heart") {
        $("#donation_request_quantity_input").val(1);
        // $("#donation_request_quantity_input").attr("disabled", true);
    } else if ($("#donation_request_organ_name_input").val() == "Liver") {
        $("#donation_request_quantity_input").val(1);
        // $("#donation_request_quantity_input").attr("disabled", true);
    } else if ($("#donation_request_organ_name_input").val() == "Pancreas") {
        $("#donation_request_quantity_input").val(1);
        // $("#donation_request_quantity_input").attr("disabled", true);
    } else if ($("#donation_request_organ_name_input").val() == "Intestines") {
        $("#donation_request_quantity_input").val(1);
        // $("#donation_request_quantity_input").attr("disabled", true);
    }
    // Living Donations
    else if ($("#donation_request_organ_name_input").val() == "Lungs") {
        $("#donation_request_quantity_input").val(1);
        // $("#donation_request_quantity_input").attr("disabled", false);
    } else if ($("#donation_request_organ_name_input").val() == "Kidney") {
        $("#donation_request_quantity_input").val(1);
        // $("#donation_request_quantity_input").attr("disabled", false);
    } else {
        // $("#donation_request_quantity_input").attr("disabled", false);
    }
}


$(document).ready(function () {
    if ($("#donation_request_donation_type_input").val() == 0) {
        $("#donation_request_tissue_name_input-group").addClass("hidden");
        $("#donation_request_organ_name_input-group").addClass("hidden");
        $("#donation_request_organ_name_input").attr("required", false);
        $("#donation_request_tissue_name_input").attr("required", false);
        $("#donation_request_quantity_input-group").removeClass("hidden");
        $("#donation_request_quantity_input").attr("required", true);
        $("#quantity_priority").html("(required)");
        $("#quantity_priority").addClass("text-info");
        $("#donation_request_quantity_input").val(1);
        // $("#donation_request_quantity_input").attr("disabled", true);
        $("#donation_request_tissue_name_input").val("");
        $("#donation_request_organ_name_input").val("");
        // console.log($("#donation_request_donation_type_input").val());
    } else if ($("#donation_request_donation_type_input").val() == 1) {
        $("#donation_request_tissue_name_input-group").addClass("hidden");
        $("#donation_request_organ_name_input-group").removeClass("hidden");
        $("#organ_name_priority").html("(required)");
        $("#organ_name_priority").addClass("text-info");
        $("#donation_request_organ_name_input").attr("required", true);
        $("#donation_request_tissue_name_input").attr("required", false);
        $("#donation_request_quantity_input-group").removeClass("hidden");
        $("#donation_request_quantity_input").attr("required", true);
        $("#quantity_priority").html("(required)");
        $("#quantity_priority").addClass("text-info");
        $("#donation_request_quantity_input").val(1);
        $("#donation_request_tissue_name_input").val("");
        // console.log($("#donation_request_donation_type_input").val());
    } else if ($("#donation_request_donation_type_input").val() == 2) {
        $("#donation_request_tissue_name_input-group").removeClass("hidden");
        $("#tissue_name_priority").html("(required)");
        $("#tissue_name_priority").addClass("text-info");
        $("#donation_request_organ_name_input").attr("required", false);
        $("#donation_request_tissue_name_input").attr("required", true);
        $("#donation_request_organ_name_input-group").addClass("hidden");
        $("#donation_request_quantity_input-group").addClass("hidden");
        $("#donation_request_quantity_input").attr("required", false);
        $("#donation_request_quantity_input").val("");
        $("#donation_request_organ_name_input").val("");
        // console.log($("#donation_request_donation_type_input").val());
    } else {
        $("#donation_request_tissue_name_input-group").addClass("hidden");
        $("#donation_request_organ_name_input-group").addClass("hidden");
        $("#donation_request_blood_group_input-group").addClass("hidden");
        $("#donation_request_quantity_input-group").addClass("hidden");
        $("#donation_request_quantity_input").val("");
        $("#donation_request_tissue_name_input").val("");
        $("#donation_request_organ_name_input").val("");
        $("#donation_request_blood_group_input").val("");
    }

    if ($("#donation_request_organ_name_input").val() == "Heart") {
        $("#donation_request_quantity_input").val(1);
        // $("#donation_request_quantity_input").attr("disabled", true);
    } else if ($("#donation_request_organ_name_input").val() == "Liver") {
        $("#donation_request_quantity_input").val(1);
        // $("#donation_request_quantity_input").attr("disabled", true);
    } else if ($("#donation_request_organ_name_input").val() == "Pancreas") {
        $("#donation_request_quantity_input").val(1);
        // $("#donation_request_quantity_input").attr("disabled", true);
    } else if ($("#donation_request_organ_name_input").val() == "Intestines") {
        $("#donation_request_quantity_input").val(1);
        // $("#donation_request_quantity_input").attr("disabled", true);
    }
    // Living Donations
    else if ($("#donation_request_organ_name_input").val() == "Lungs") {
        $("#donation_request_quantity_input").val(1);
        // $("#donation_request_quantity_input").attr("disabled", false);
    } else if ($("#donation_request_organ_name_input").val() == "Kidney") {
        $("#donation_request_quantity_input").val(1);
        // $("#donation_request_quantity_input").attr("disabled", false);
    } else {
        // $("#donation_request_quantity_input").attr("disabled", false);
    }

});