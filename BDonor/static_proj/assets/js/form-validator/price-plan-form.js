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

// Force to enter only numeric
$("#plan_amount_input").inputFilter(function (value) {
    return /^\d*$/.test(value);
});
// // Force to enter only float
// $("#plan_amount_input").inputFilter(function (value) {
//     return /^-?\d*[.,]?\d*$/.test(value);
// });