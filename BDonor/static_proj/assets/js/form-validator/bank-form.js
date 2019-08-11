var form = $("#donationBank_manage_form");

// force to enter only number 0-9
// (function ($) {
//     $.fn.inputFilter = function (inputFilter) {
//         return this.on(
//             "input keydown keyup mousedown mouseup select contextmenu drop",
//             function () {
//                 if (inputFilter(this.value)) {
//                     this.oldValue = this.value;
//                     this.oldSelectionStart = this.selectionStart;
//                     this.oldSelectionEnd = this.selectionEnd;
//                 } else if (this.hasOwnProperty("oldValue")) {
//                     this.value = this.oldValue;
//                     this.setSelectionRange(this.oldSelectionStart, this.oldSelectionEnd);
//                 }
//             }
//         );
//     };
// })(jQuery);

// $("#bank_contact_input").inputFilter(function (value) {
//     return /^\d*$/.test(value);
// });

// form.find('select, textarea, input').each(function () {
//     console.log($(this).attr('name'));
// });


// preventing form from autocomplete
$(document).ready(function () {
    $(document).on("focus", ":input", function () {
        $(this).attr("autocomplete", "off");
    });
});