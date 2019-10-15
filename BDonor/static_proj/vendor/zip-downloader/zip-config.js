var Promise = window.Promise;
if (!Promise) {
  Promise = JSZip.external.Promise;
}

/**
 * Fetch the content and return the associated promise.
 * @param {String} url the url of the content to fetch.
 * @return {Promise} the promise containing the data.
 */
function urlToPromise(url) {
  return new Promise(function(resolve, reject) {
    JSZipUtils.getBinaryContent(url, function(err, data) {
      if (err) {
        reject(err);
      } else {
        resolve(data);
      }
    });
  });
}

var box = document.getElementsByTagName("input");

$("#check-all").click(function() {
  var values = [];
  for (i = 0; i < box.length; i++) {
    if (box[i].checked == true) {
      values.push(box[i].value);
    }
  }
  if (values.length >= 1) {
    $("#dflt").addClass("hidden");
    $("#chkd").addClass("hidden");
    $("#uchkd").removeClass("hidden");
    $(".check-box").prop("checked", false);
    $("#download_btn").addClass("hidden");
    $("#cancel_btn").addClass("hidden");
  } else {
    $("#dflt").addClass("hidden");
    $("#chkd").removeClass("hidden");
    $("#uchkd").addClass("hidden");
    $(".check-box").prop("checked", true);
    $("#download_btn").removeClass("hidden");
    $("#cancel_btn").removeClass("hidden");
  }
  resetMessage();
  $("#progress_bar").addClass("hidden");
});

$(box).click(function() {
  var values = [];
  for (i = 0; i < box.length; i++) {
    if (box[i].checked == true) {
      values.push(box[i].value);
    }
  }
  if (values.length >= 1) {
    $("#download_btn").removeClass("hidden");
    $("#cancel_btn").removeClass("hidden");
  } else {
    $("#download_btn").addClass("hidden");
    $("#cancel_btn").addClass("hidden");
  }
  resetMessage();
  $("#progress_bar").addClass("hidden");
  // if ('.check-box:checked') {
  //     var $this = $(this);
  //     var tmpname = $this.data("title");
  //     var li = document.createElement("li");
  //     li.classList.add("text-danger");
  //     li.setAttribute("id", $this.data("slug"));
  //     var node = document.createTextNode(tmpname);
  //     li.appendChild(node);
  //     var element = document.getElementById("ul1");
  //     element.appendChild(li);
  // }
  // else {
  //     var $this = $(this);
  //     var slug = $this.data("slug");
  //     var input_id = document.getElementById(slug);
  //     input_id.style.display = "none";
  // }
});

//var $form = $("#download_form").on("submit", function () {
$("#download_btn").click(function() {
  resetMessage();

  // Custom
  var inputs = document.getElementsByTagName("input");
  var values = [];
  for (i = 0; i < inputs.length; i++) {
    if (inputs[i].checked == true) {
      values.push(inputs[i].value);
    }
  }
  // console.log(values.join());
  // alert(values.length);
  // Custom

  if (values.length >= 1) {
    var zip = new JSZip();

    // find every checked item
    $.each($(".check-box:checked"), function() {
      var $this = $(this);
      var url = $this.data("url");
      // alert(url);
      var filename = url.replace(/.*\//g, "");
      zip.file(filename, urlToPromise(url), {
        binary: true
      });
    });

    // when everything has been downloaded, we can trigger the dl
    zip
      .generateAsync(
        {
          type: "blob"
        },
        function updateCallback(metadata) {
          var msg = "progression : " + metadata.percent.toFixed(2) + " %";
          if (metadata.currentFile) {
            msg += ", current file = " + metadata.currentFile;
          }
          showMessage(msg);
          updatePercent(metadata.percent | 0);
        }
      )
      .then(
        function callback(blob) {
          // see FileSaver.js
          var d = new Date();
          var year = d.getFullYear();

          var zip_name = $("#zip-name").val();

          saveAs(blob, "BDonor-Blog_" + zip_name + "-" + year + ".zip");

          showMessage("Zip File Downloaded Successfully !!!");

          $(".check-box").prop("checked", false);

          $("#clear_btn").removeClass("hidden");
          $("#zip_btn_div").addClass("hidden");
        },
        function(e) {
          showError(e);
        }
      );

    return false;
  } else {
    showError("You must select at least one file to download as zip!");
    $("#progress_bar").addClass("hidden");
  }
});

// ========================= Download All Selected Contributions =========================
$("#download_all_btn").click(function() {
  resetMessage();

  var zip = new JSZip();
  
  $.each($(".download-all-check-box:checked"), function() {
    var $this = $(this);
    var url = $this.data("url");
    // alert(url);
    var filename = url.replace(/.*\//g, "");
    zip.file(filename, urlToPromise(url), {
      binary: true
    });
  });

  // when everything has been downloaded, we can trigger the dl
  zip
    .generateAsync(
      {
        type: "blob"
      },
      function updateCallback(metadata) {
        var msg = "progression : " + metadata.percent.toFixed(2) + " %";
        if (metadata.currentFile) {
          msg += ", current file = " + metadata.currentFile;
        }
        showMessage(msg);
        updatePercent(metadata.percent | 0);
      }
    )
    .then(
      function callback(blob) {
        // see FileSaver.js
        var d = new Date();
        var year = d.getFullYear();

        var zip_name = $("#zip-name").val();

        saveAs(blob, "BDonor-Blog_" + zip_name + "-" + year + ".zip");

        showMessage("Zip File Downloaded Successfully !!!");

        $(".check-box").prop("checked", false);

        $("#clear_btn").removeClass("hidden");
        $("#zip_btn_div").addClass("hidden");
      },
      function(e) {
        showError(e);
      }
    );

  return false;
});

/**
 * Reset the message.
 */
function resetMessage() {
  $("#result")
    .removeClass()
    .text("");
}
/**
 * show a successful message.
 * @param {String} text the text to show.
 */
function showMessage(text) {
  resetMessage();
  $("#result")
    .addClass("alert alert-success text-center")
    .text(text);
}
/**
 * show an error message.
 * @param {String} text the text to show.
 */
function showError(text) {
  resetMessage();
  $("#result")
    .addClass("alert alert-danger text-center")
    .text(text);
}
/**
 * Update the progress bar.
 * @param {Integer} percent the current percent
 */
function updatePercent(percent) {
  $("#progress_bar")
    .removeClass("hidden")
    .find(".progress-bar")
    .attr("aria-valuenow", percent)
    .css({
      width: percent + "%"
    });
}

// if (!JSZip.support.blob) {
//     showError("This demo works only with a recent browser !");
//     return;
// }

$("#clear_btn").click(function() {
  $("#zip_div").addClass("hidden");
});
$("#cancel_btn").click(function() {
  $("#zip_div").addClass("hidden");
});
