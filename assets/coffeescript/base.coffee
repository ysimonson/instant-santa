$("img").error(() ->
    $(this).replaceWith($("<div>Well this is awkward, but um... I couldn't find your face...</div>"))
)