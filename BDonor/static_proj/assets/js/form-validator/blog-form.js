$(document).ready(function () {

    var remaining_upload = $("#upload_remaining").val();

    // console.log(remaining_upload);

    if (remaining_upload == "") {
        remaining_upload = 3
    };

    if (remaining_upload > 0) {

        $('#blog_file_input').fileinput({
            // allowedFileTypes: ['image', 'html', 'text', 'video', 'audio', 'flash', 'object'],
            allowedFileTypes: ['image', 'html', 'text', 'office', 'pdf'],
            allowedFileExtensions: ['jpg', 'jpeg', 'png', 'pdf', 'doc', 'docx'],
            // allowedPreviewTypes: ['image', 'html', 'text', 'video', 'audio', 'flash', 'object'],
            allowedPreviewTypes: ['image', 'html', 'text', 'office', 'pdf'],
            disabledPreviewTypes: ['jpg', 'jpeg', 'png', 'pdf', 'doc', 'docx'],
            // resizeImage: true,
            // maxImageWidth: 200,
            // maxImageHeight: 200,
            // resizePreference: 'width',
            maxFileSize: 1536, //KB
            // maxFilePreviewSize: 6,
            // minFileCount: 1,
            maxFileCount: remaining_upload,
            maxTotalFileCount: remaining_upload,
            // resizeImageQuality: 0.93,
            showCaption: true,
            showPreview: true,
            showRemove: true,
            showUploadStats: true,
            showCancel: true,
            showPause: true,
            showClose: true,
            showUploadedThumbs: true,
            showBrowse: true,
            removeFromPreviewOnError: true,
            showUpload: false,
            browseOnZoneClick: true,
            autoReplace: true,
            purifyHtml: true,
            autoOrientImage: function () {
                var ua = window.navigator.userAgent,
                    webkit = !!ua.match(/WebKit/i),
                    iOS = !!ua.match(/iP(od|ad|hone)/i),
                    iOSSafari = iOS && webkit && !ua.match(/CriOS/i);
                return !iOSSafari;
            },
            previewZoomButtonIcons: {
                prev: '<i class="fas fa-chevron-left"></i>',
                next: '<i class="fas fa-chevron-right"></i>',
                toggleheader: '<i class="fas fa-arrows-alt-v"></i>',
                fullscreen: '<i class="fas fa-expand"></i>',
                borderless: '<i class="fas fa-external-link-square-alt"></i>',
                close: '<i class="fas fa-times"></i>'
            },
            previewFileIcon: '<i class="fas fa-eye"></i>',
            previewFileIconSettings: {
                'doc': '<i class="fa fa-file-word-o text-primary"></i>',
                'xls': '<i class="fa fa-file-excel-o text-success"></i>',
                'ppt': '<i class="fa fa-file-powerpoint-o text-danger"></i>',
                'jpg': '<i class="fa fa-file-photo-o text-warning"></i>',
                'pdf': '<i class="fa fa-file-pdf-o text-danger"></i>',
                'zip': '<i class="fa fa-file-archive-o text-muted"></i>',
            },
            browseLabel: 'Browse',
            captionClass: 'text-info',
            // initialCaption: 'Select files (Max:3)',
            msgPlaceholder: "Select files (Max:" + remaining_upload + ")",
            buttonLabelClass: 'text-white',
            browseIcon: '<i class="fas fa-folder-open"></i>',
            browseClass: 'btn btn-dark',
            removeLabel: 'Remove',
            removeIcon: '<i class="fas fa-trash-alt"></i>',
            removeClass: 'btn btn-danger',
            cancelIcon: '<i class="fas fa-times"></i>',
            pauseIcon: '<i class="fas fa-stop-circle"></i>',
            uploadIcon: '<i class="fas fa-cloud-upload-alt"></i>',
            zoomIndicator: '<i class="fas fa-search-plus"></i>',
            zoomIcon: '<i class="fas fa-search-plus"></i>',
            // dragIcon: '<i class="fas fa-search-plus"></i>',
            // zoomModalHeight: 480,
            // minImageHeight: null,
            // maxImageHeight: null,
            // minImageWidth: null,
            // maxImageWidth: null,
            // showDrag: true,
            // previewSettings: {
            //     image: {
            //         width: "auto",
            //         height: "auto",
            //         'max-width': "100%",
            //         'max-height': "100%"
            //     },
            //     html: {
            //         width: "213px",
            //         height: "160px"
            //     },
            //     text: {
            //         width: "213px",
            //         height: "160px"
            //     },
            //     office: {
            //         width: "213px",
            //         height: "160px"
            //     },
            //     gdocs: {
            //         width: "213px",
            //         height: "160px"
            //     },
            //     video: {
            //         width: "213px",
            //         height: "160px"
            //     },
            //     audio: {
            //         width: "100%",
            //         height: "30px"
            //     },
            //     flash: {
            //         width: "213px",
            //         height: "160px"
            //     },
            //     object: {
            //         width: "213px",
            //         height: "160px"
            //     },
            //     pdf: {
            //         width: "213px",
            //         height: "160px"
            //     },
            //     other: {
            //         width: "213px",
            //         height: "160px"
            //     }
            // },
            // previewSettingsSmall: {
            //     image: {
            //         width: "auto",
            //         height: "auto",
            //         'max-width': "100%",
            //         'max-height': "100%"
            //     },
            //     html: {
            //         width: "100%",
            //         height: "160px"
            //     },
            //     text: {
            //         width: "100%",
            //         height: "160px"
            //     },
            //     office: {
            //         width: "100%",
            //         height: "160px"
            //     },
            //     gdocs: {
            //         width: "100%",
            //         height: "160px"
            //     },
            //     video: {
            //         width: "100%",
            //         height: "auto"
            //     },
            //     audio: {
            //         width: "100%",
            //         height: "30px"
            //     },
            //     flash: {
            //         width: "100%",
            //         height: "auto"
            //     },
            //     object: {
            //         width: "100%",
            //         height: "auto"
            //     },
            //     pdf: {
            //         width: "100%",
            //         height: "160px"
            //     },
            //     other: {
            //         width: "100%",
            //         height: "160px"
            //     }
            // },
            // previewZoomSettings: {
            //     image: {
            //         width: "auto",
            //         height: "auto",
            //         'max-width': "100%",
            //         'max-height': "100%"
            //     },
            //     html: {
            //         width: "100%",
            //         height: "100%",
            //         'min-height': "480px"
            //     },
            //     text: {
            //         width: "100%",
            //         height: "100%",
            //         'min-height': "480px"
            //     },
            //     office: {
            //         width: "100%",
            //         height: "100%",
            //         'max-width': "100%",
            //         'min-height': "480px"
            //     },
            //     gdocs: {
            //         width: "100%",
            //         height: "100%",
            //         'max-width': "100%",
            //         'min-height': "480px"
            //     },
            //     video: {
            //         width: "auto",
            //         height: "100%",
            //         'max-width': "100%"
            //     },
            //     audio: {
            //         width: "100%",
            //         height: "30px"
            //     },
            //     flash: {
            //         width: "auto",
            //         height: "480px"
            //     },
            //     object: {
            //         width: "auto",
            //         height: "480px"
            //     },
            //     pdf: {
            //         width: "100%",
            //         height: "100%",
            //         'min-height': "480px"
            //     },
            //     other: {
            //         width: "auto",
            //         height: "100%",
            //         'min-height': "480px"
            //     }
            // },
        });
    }
    else{
        $("#blog_file_input").addClass("hidden");
    }
});