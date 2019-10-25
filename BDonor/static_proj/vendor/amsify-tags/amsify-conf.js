$(document).ready(function () {
    $('input[name="tags"]').amsifySuggestags({
        type: 'bootstrap', //bootstrap, materialize, amsify
        // suggestions: ['Black', 'White', 'Red', 'Blue', 'Green', 'Orange']
        tagLimit: 5,
        // noSuggestionMsg: '',
        // classes: [],
        // backgrounds: [],
        // colors: [],
        // whiteList: true,
        // selectOnHover: true,
        // afterAdd: function (value) {
        //     //
        // },
        // afterRemove: function (value) {
        //     //
        // }
        // suggestionsAction: {
        //     url: '/path/to/suggestions/',
        //     beforeSend: function () {
        //         console.info('beforeSend');
        //     },
        //     success: function (data) {
        //         console.info('success');
        //     },
        //     error: function () {
        //         console.info('error');
        //     },
        //     complete: function (data) {
        //         console.info('complete');
        //     }
        // }
    });
});