###
# Browser page.
###

begin_time = null
end_time = null
slider_ticks = 100000

info = ->
    ###
    # Query for server info and create slider.
    ###
    
    
    $.ajax 'range?amount=3600',
        dataType : 'json'
        cache    : false
        timeout  : 2000
        success  : (data, status, req) ->
            begin_time = data.begin_time
            end_time = data.end_time
            $('#begin_time').text begin_time
            $('#end_time').text end_time
            create_slider()
        error : (req, status, err) ->
            info()
        complete : (req, satus) ->

onImageLoad = ->
    ###
    #
    ###
    null
    
on_slide = (amount) ->
    ###
    # Do AJAX associated with slider movement.
    ###

    $('#slider_amount').text amount.toFixed(3)

    url = 'slide?time1=' + begin_time + '&time2=' + end_time + '&amount=' + amount
    $.ajax url,
        async    : false
        dataType : 'json'
        cache    : false
        timeout  : 2000
        success  : (data, status, req) ->
            $('#latest_image').attr 'src', data.result_url
            $('#current_time').text data.result_time
        error : (req, status, err) ->
            null
        complete : (req, satus) ->
            null

create_slider = ->
    ###
    # Create the slider widget, given the size.
    ###
    $('#slider').slider
        min: 0
        max: slider_ticks-1
        value: slider_ticks/2
        create: (event, ui) ->
            on_slide(0.5)
        slide: (event, ui) ->
            on_slide(ui.value/(slider_ticks-1))
    $('#slider').bind 'keydown', (event) ->
        null
        
$ ->
    ###
    # Run when document has loaded.
    ###
    info()

# All CoffeeScript output is wrapped in an anonymous function,
# so in order to use functions as top-level variables (like in HTML)
# let's attach them as properties on *window*.
window.wabbitOnImageLoad = onImageLoad

