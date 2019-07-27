var page_title = $("#page_title").val();
var form = $("#donation_filter_form");
var searchBtn = $("#donation_search_btn");

searchBtn.click(function (event) {
    event.preventDefault();
    // console.log("Worked");
    form.submit();
    return true;
});
