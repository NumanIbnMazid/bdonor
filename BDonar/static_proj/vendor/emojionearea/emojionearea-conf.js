$(document).ready(function() {
  $("#chat_box_input").emojioneArea({
    emojiPlaceholder: ":smile_cat:",
    placeholder: "Type your message...",
    // container: $("#emojione_container"),
    recentEmojis: true,
    pickerPosition: "top",
    filtersPosition: "top",
    search: true,
    searchPosition: "bottom",
    searchPlaceholder: "Search",
    hidePickerOnBlur: true,
    tones: true,
    tonesStyle: "checkbox", // 'bullet' | 'radio' | 'square' | 'checkbox'
    shortnames: false,
    hideSource: true,
    inline: null, // null | true | false
    useInternalCDN: true,
    shortcuts: true,
    autocomplete: true,
    autocompleteTones: false,
    buttonTitle: "Use the TAB key to insert emoji faster",
    attributes: {
      spellcheck: true,
      autocomplete: "on"
    }
  });
});
