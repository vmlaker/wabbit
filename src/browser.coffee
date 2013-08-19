###
# Browser page.
###

info = ->
    ###
    # Query for server info and create slider.
    ###
    $.ajax 'service/info',
        dataType : 'json'
        cache    : false
        timeout  : 2000
        success  : (data, status, req) ->
            create_slider(data.db_size)
        error : (req, status, err) ->
            info()
        complete : (req, satus) ->
            null
                    
create_slider = (size) ->
    ###
    # Create the slider widget, given the size.
    ###
    $('#slider').slider
        min: 0
        max: size-1
        value: size/2
        create: (event, ui) ->
            $('#slider_value').text parseInt(size/2)
            $('#slider_min').text 0
            $('#slider_max').text size-1
        slide: (event, ui) ->
            $('#slider_value').text ui.value
            
$ ->
    ###
    # Run when document has loaded.
    ###
    info()
