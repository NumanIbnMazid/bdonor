


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
$("#card_number").inputFilter(function (value) {
    return /^\d*$/.test(value);
});
$("#exp_month").inputFilter(function (value) {
    return /^\d*$/.test(value);
});
$("#exp_year").inputFilter(function (value) {
    return /^\d*$/.test(value);
});
$("#cvc").inputFilter(function (value) {
    return /^\d*$/.test(value);
});

// force to enter only number between specific
$("#exp_month").inputFilter(function (value) {
    return /^\d*$/.test(value) && (value === "" || parseInt(value) <= 12);
});
$("#exp_year").inputFilter(function (value) {
    return /^\d*$/.test(value) && (value === "" || parseInt(value) <= 2050);
});

// force to match the minimum and maximum length
$("#card_number").keypress(function (e) {
    var max = $("#card_number").attr("maxlength");
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
$("#exp_month").keypress(function (e) {
    var max = $("#exp_month").attr("maxlength");
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
$("#exp_year").keypress(function (e) {
    var max = $("#exp_year").attr("maxlength");
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





// preventing form from autocomplete
$(document).ready(function () {
    $(document).on("focus", ":input", function () {
        $(this).attr("autocomplete", "off");
    });
});