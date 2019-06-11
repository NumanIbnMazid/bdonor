//  @@@@@@@@@@@@@@@@@@@ CONTACT 1 @@@@@@@@@@@@@@@@@@@

$("#donation_contact_input").intlTelInput({
  initialCountry: "bd", //auto
  nationalMode: false,
  preferredCountries: ["bd", "us"],
  separateDialCode: true,
  formatOnDisplay: false
});

//  @@@@@@@@@@@@@@@@@@@ CONTACT 2 @@@@@@@@@@@@@@@@@@@

$("#donation_contact2_input").intlTelInput({
    initialCountry: "bd", //auto
    nationalMode: false,
    preferredCountries: ["bd", "us"],
    separateDialCode: true,
    formatOnDisplay: false
  });

  //  @@@@@@@@@@@@@@@@@@@ CONTACT 3 @@@@@@@@@@@@@@@@@@@

$("#donation_contact3_input").intlTelInput({
    initialCountry: "bd", //auto
    nationalMode: false,
    preferredCountries: ["bd", "us"],
    separateDialCode: true,
    formatOnDisplay: false
  });

// ========================= HELPERS ==========================

// Vanilla Javascript
// var input = document.querySelector("#donation_contact_input");
// window.intlTelInput(input, {
//     // https://www.jqueryscript.net/form/jQuery-International-Telephone-Input-With-Flags-Dial-Codes.html

//     // whether or not to allow the dropdown
//     //   allowDropdown: true,

//     // if there is just a dial code in the input: remove it on blur, and re-add it on focus
//     //   autoHideDialCode: true,

//     // add a placeholder in the input with an example number for the selected country
//     //   autoPlaceholder: "polite",

//     // modify the auto placeholder
//     //   customPlaceholder: null,

//     // append menu to specified element
//     //   dropdownContainer: null,

//     // don't display these countries
//     //   excludeCountries: [],

//     // format the input value during initialisation and on setNumber
//     //   formatOnDisplay: true,

//     // geoIp lookup function
//     //   geoIpLookup: null,

//     // inject a hidden input with this name, and on submit, populate it with the result of getNumber
//     //   hiddenInput: "",

//     // initial country
//     initialCountry: "bd", //auto

//     // localized country names e.g. { 'de': 'Deutschland' }
//     //   localizedCountries: null,

//     // don't insert international dial codes
//     // nationalMode: false,

//     // display only these countries
//     //   onlyCountries: [],

//     // number type to use for placeholders
//     //   placeholderNumberType: "MOBILE",

//     // the countries at the top of the list. defaults to united states and united kingdom
//     preferredCountries: ["bd", "us"],

//     // display the country dial code next to the selected flag so it's not part of the typed number
//     // separateDialCode: true,

//     // specify the path to the libphonenumber script to enable validation/formatting
//     // utilsScript: "https://cdnjs.cloudflare.com/ajax/libs/intl-tel-input/11.0.4/js/utils.js",
//     // utilsScript: "https://intl-tel-input.com/node_modules/intl-tel-input/build/js/utils.js",
//     // utilsScript: "",
// });

// jQuery -------------------------------------

// $("#donation_contact_input").intlTelInput({
//   // https://www.jqueryscript.net/form/jQuery-International-Telephone-Input-With-Flags-Dial-Codes.html

//   // whether or not to allow the dropdown
//   //   allowDropdown: true,

//   // if there is just a dial code in the input: remove it on blur, and re-add it on focus
//   //   autoHideDialCode: true,

//   // add a placeholder in the input with an example number for the selected country
//   //   autoPlaceholder: "polite",

//   // modify the auto placeholder
//   //   customPlaceholder: null,

//   // append menu to specified element
//   //   dropdownContainer: null,

//   // don't display these countries
//   //   excludeCountries: [],

//   // format the input value during initialisation and on setNumber
//   //   formatOnDisplay: true,

//   // geoIp lookup function
//   //   geoIpLookup: null,

//   // inject a hidden input with this name, and on submit, populate it with the result of getNumber
//   //   hiddenInput: "",

//   // initial country
//   initialCountry: "bd", //auto

//   // localized country names e.g. { 'de': 'Deutschland' }
//   //   localizedCountries: null,

//   // don't insert international dial codes
//   nationalMode: false,

//   // display only these countries
//   //   onlyCountries: [],

//   // number type to use for placeholders
//   //   placeholderNumberType: "MOBILE",

//   // the countries at the top of the list. defaults to united states and united kingdom
//   preferredCountries: ["bd", "us"],

//   // display the country dial code next to the selected flag so it's not part of the typed number
//   separateDialCode: true

//   // specify the path to the libphonenumber script to enable validation/formatting
//   // utilsScript: "https://cdnjs.cloudflare.com/ajax/libs/intl-tel-input/11.0.4/js/utils.js",
//   // utilsScript: "https://intl-tel-input.com/node_modules/intl-tel-input/build/js/utils.js",
//   // utilsScript: "",
// });

// ================= API Methods =================
// // destroy
// instance.destroy();

// // Get the extension part of the current number
// var extension = instance.getExtension();

// // Get the current number in the given format
// var intlNumber = instance.getNumber();

// // Get the type (fixed-line/mobile/toll-free etc) of the current number.
// var numberType = instance.getNumberType();

// // Get the country data for the currently selected flag.
// var countryData = instance.getSelectedCountryData();

// // Get more information about a validation error.
// var error = instance.get < a href = "https://www.jqueryscript.net/tags.php?/Validation/" > Validation < /a>Error();

// // Vali<a href="https://www.jqueryscript.net/time-clock/">date</a> the current number
// var isValid = instance.isValidNumber();

// // Change the country selection
// instance.selectCountry("gb");

// // Insert a number, and update the selected flag accordingly.
// instance.setNumber("+44 7733 123 456");

// // Change the placeholderNumberType option.
// instance..setPlaceholderNumberType("FIXED_LINE");

// // Load the utils.js script (included in the lib directory) to enable formatting/validation etc.
// window.intlTelInputGlobals.loadUtils("build/js/utils.js");

// // Get all the country data
// var countryData = window.intlTelInputGlobals.getCountryData();

// ================= Event Handlers =================
// input.addEventListener("countrychange", function() {
//   // do something with iti.getSelectedCountryData()
// });

// input.addEventListener("open:countrydropdown", function() {
//   // triggered when the user opens the dropdown
// });

// input.addEventListener("close:countrydropdown", function() {
//   // triggered when the user closes the dropdown
// });
