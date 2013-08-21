###
# Browser page.
###

begin_time = null
end_time = null
slider_ticks = 1000

info = ->
    ###
    # Query for server info and create slider.
    ###
    
    
    $.ajax 'service/range?amount=3600',
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
    
on_slide = (value) ->
    ###
    # Do AJAX associated with slider movement.
    ###

    url = 'service/slide?time1=' + begin_time + '&time2=' + end_time + '&amount=' + value
    $.ajax url,
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
            $('#slider_value').text parseInt(slider_ticks/2)
            $('#slider_min').text 0
            $('#slider_max').text slider_ticks-1
            on_slide(0.5)
        slide: (event, ui) ->
            amount = ui.value/slider_ticks
            on_slide(amount)
            $('#slider_value').text ui.value
            $('#slider_amount').text amount

                        
$ ->
    ###
    # Run when document has loaded.
    ###
    info()

# All CoffeeScript output is wrapped in an anonymous function,
# so in order to use functions as top-level variables (like in HTML)
# let's attach them as properties on *window*.
window.wabbitOnImageLoad = onImageLoad

