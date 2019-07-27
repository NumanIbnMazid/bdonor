//Django basic setup for accepting ajax requests.
// Cookie obtainer Django

function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    var cookies = document.cookie.split(";");
    for (var i = 0; i < cookies.length; i++) {
      var cookie = jQuery.trim(cookies[i]);
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
var csrftoken = getCookie("csrftoken");
// Setup ajax connections safetly

function csrfSafeMethod(method) {
  // these HTTP methods do not require CSRF protection
  return /^(GET|HEAD|OPTIONS|TRACE)$/.test(method);
}
$.ajaxSetup({
  beforeSend: function(xhr, settings) {
    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
      xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
  }
});






// AJAX EXAMPLE

// $.ajax({
//   url: endpoint, // the endpoint
//   type: "POST", // http method
//   data: {
//     title: $("#donation_title_input").val(),
//     type: $("#donation_type_input").val(),
//     custom_type: $("#donation_custom_type_input").val(),
//     blood_group: $("#donation_blood_group_input").val(),
//     blood_bag: $("#donation_blood_bag_input").val(),
//     organ_name: $("#donation_organ_name_input").val(),
//     details: $("#donation_details_input").val(),
//     details_fake: $("#donation_details_fake_input").val(),
//     contact: $("#donation_contact_input").val(),
//     contact2: $("#donation_contact2_input").val(),
//     contact3: $("#donation_contact3_input").val(),
//     preferred_date: $("#donation_preferred_date_input").val(),
//     preferred_date_from: $("#donation_preferred_date_from_input").val(),
//     preferred_date_to: $("#donation_preferred_date_to_input").val(),
//     location: $("#donation_location_input").val(),
//     priority: $("#donation_priority_input").val(),
//     publication_status: $("#donation_publication_status_input").val(),
//   },

//   // data: serializedData,
  
//   success: function(json) {
//     console.log(json);
//     // console.log("success");
//     // console.log(data);
//     form[0].reset();
//   },

//   error: function(xhr, errmsg, err) {
//     console.log(xhr.status + ": " + xhr.responseText);
//   }
// });