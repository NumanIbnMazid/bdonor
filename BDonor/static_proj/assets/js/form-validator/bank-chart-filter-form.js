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

    // function checkDate() {
    //     var input = $("#date_to");
    //     return input.val();
    // }

    $("#date_from").datetimepicker({
        timepicker: false,
        format: "Y-m-d",
        // maxDate: now(),
        validateOnBlur: true,
        closeOnDateSelect:true,
        todayButton: true,
        // onShow: function (ct) {
        //     this.setOptions({
        //         // maxDate: jQuery('#date_to').val() ? jQuery('#date_to').val() : false,
        //         maxDate: checkDate()
        //     })
        // },
    });
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

    // function checkDate(){
    //     var input = $("#date_from");
    //     return input.val();
    // }

    $("#date_to").datetimepicker({
        timepicker: false,
        format: "Y-m-d",
        // maxDate: now(),
        validateOnBlur: true,
        closeOnDateSelect:true,
        todayButton: true,
        // onShow: function (ct) {
        //     this.setOptions({
        //         // maxDate: jQuery('#date_from').val() ? jQuery('#date_to').val() : false,
        //         maxDate: checkDate()
        //     })
        // },
    });
});

// preventing form from autocomplete
$(document).ready(function () {
    $(document).on("focus", ":input", function () {
        $(this).attr("autocomplete", "off");
    });
});

function resetMessage() {
    $(".error").html("");
}

function dateFilterFunction() {
    // resetMessage();
    var date_from_input = $("#date_from");
    var date_to_input = $("#date_to");
    // console.log(date_from_input);
    // console.log(date_to_input);
    var df = date_from_input.val().split("-");
    var dt = date_to_input.val().split("-");
    // console.log(df);
    // console.log(dt);
    var df_j = df.join(' ');
    var dt_j = dt.join(' ');
    // console.log(df_j);
    // console.log(dt_j);
    var date_f = new Date(df_j);
    var date_t = new Date(dt_j);
    // console.log(date_f);
    // console.log(date_t);
    if (date_from_input.val() == "" && date_to_input.val() != ""){
        $("#from_error_msg").html("This field is required !");
        $("#bank_chart_filter_form").submit(function (e) {
            e.preventDefault();
        });
    }
    else if (date_f > date_t) {
        $("#error_msg").html("From Date must be smaller than or equal To Date!");
        $("#bank_chart_filter_form").submit(function (e) {
            e.preventDefault();
        });
    }
    else {
        // console.log("Perfect !!!");
        $("#bank_chart_filter_form").submit(function (e) {
            e.preventDefault();
            $('#bank_chart_filter_form').unbind('submit').submit();
        });
    }
    if (date_to_input.val() == "") {
        $("#from_error_msg").html("");
        $("#error_msg").html("");
    }
    if (date_to_input.val() != "" && date_from_input.val() != "") {
        $("#from_error_msg").html("");
        $("#to_error_msg").html("");
    }
}