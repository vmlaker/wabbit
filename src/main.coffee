###
# AJAX call for main info page.
###

# Set-timeout values: current, min/max limits and adjustment coefficient.
set_timeout_cur = 100
set_timeout_max = 1000
set_timeout_min = 0
set_timeout_incr = 10
set_timeout_decr = 10

# The actual AJAX timeout value.
ajax_timeout = 2000

# Previous image timestamp, used to detect whether
# a new image is available.
prev_image_tstamp = null

# Time when image source <img src=...> changes.
# Used to compute image load time.
image_load_begin = Date.now()

# Keep track of latest interval between images.
image_interval = Date.now()

# Keep counts of requests, earlies and errors.
request_count = 0
early_count = 0
error_count = 0

info = ->
    ###
    # Make the AJAX server info request.
    ###

    # Increment the request count.
    request_count++
    
    # Mark the time-of-request.
    request_begin = Date.now()

    # Mark the beginning of callback entry.
    callback_begin = null
        
    $.ajax 'service/info',
        dataType : 'json'
        cache    : false
        timeout  : ajax_timeout
        success  : (data, status, req) ->

            # Mark the start of callback processing.
            callback_begin = Date.now()

            # Update the AJAX response time. 
            elapsed = (Date.now() - request_begin) / 1000;
            $('#response_time').text elapsed.toFixed(3)
            
            short_tstamp = data.latest_tstamp.slice(0, -7)  # Trim off ms.
            short_tstamp = short_tstamp.substring(11)  # Trim off date.
            $('#live_time_hud').text short_tstamp
            $('#server_time').text data.server_time.slice(0, -3)
            $('#load_avg').text data.load_avg
            $('#db_size').text data.db_size
            $('#latest_tstamp').text data.latest_tstamp.slice(0, -3)

            # If the database is empty, turn OFF live display
            # and try again.
            if data.db_size == '0'
                $('#live_outer').css 'display', 'none'
                tryInfoAgain()
                
            # Otherwise, if a new image arrived...
            else if prev_image_tstamp != data.latest_tstamp

                # Compute the interval between images
                # as the difference between now and the previous load.
                image_interval = Date.now() - image_load_begin
                $('#image_interval').text (image_interval/1000).toFixed(3)
                
                # Reset load begin time.
                image_load_begin = Date.now()

                # Set the <img> src attribute
                # and make sure live display is ON.
                $('#latest_image').attr 'src', data.latest_url
                $('#live_outer').css 'display', 'inline-block'
                prev_image_tstamp = data.latest_tstamp

            # Otherwise, the database is not empty but there is no
            # newer image available.
            # Either we requested too soon (the server's capture
            # framerate is slower than our request rate)
            else
                early_count++
                tryInfoAgain()

        error : (req, status, err) ->

            # Mark the start of callback processing.
            callback_begin = Date.now()

            # Increment the error count.
            error_count++
            
            # Update the AJAX response time display. 
            elapsed = (Date.now() - request_begin) / 1000;
            $('#response_time').text elapsed.toFixed(3)

            $('#server_time').text 'Error'
            $('#load_avg').text ''
            $('#db_size').text ''
            $('#latest_tstamp').text ''

            tryInfoAgain()
            
        complete : (req, satus) ->

            # Update the callback processing time display.
            elapsed = (Date.now() - callback_begin) / 1000;
            $('#callback_time').text elapsed.toFixed(3)
            
            # Update the displays.
            $('#request_count').text request_count
            $('#error_count').text error_count        
            $('#set_timeout').text (set_timeout_cur/1000).toFixed(3)

            # Update the early count display.
            ratio = request_count/early_count
            $('#early_count').text early_count
            $('#request_early_ratio').text ratio.toFixed(3)

        
tryInfoAgain = ->
    ###
    # Increase the set-timeout delay, and then
    # set info() as the timeout callback.
    ###

    # Compute the interval between images
    # as the difference between now and the previous image load.
    image_interval = Date.now() - image_load_begin
    $('#image_interval').text (image_interval/1000).toFixed(3)

    # Set timeout.
    set_timeout_cur += set_timeout_incr
    set_timeout_cur = Math.min(set_timeout_cur, set_timeout_max)
    callback = -> info 0
    setTimeout callback, set_timeout_cur


onImageLoad = ->
    ###
    # Decrease the set-timeout delay and call info().
    ###

    # Update the load-time display.
    load_time = Date.now() - image_load_begin
    $('#image_load_time').text (load_time/1000).toFixed(3)

    # Set timeout.
    set_timeout_cur -= set_timeout_decr
    set_timeout_cur = Math.max(set_timeout_cur, set_timeout_min)
    callback = -> info 0
    setTimeout callback, set_timeout_cur

# Only run when document has loaded
$ ->
    info()

# All CoffeeScript output is wrapped in an anonymous function,
# so in order to use functions as top-level variables (like in HTML)
# let's attach them as properties on *window*.
window.wabbitOnImageLoad = onImageLoad

# End of file.
