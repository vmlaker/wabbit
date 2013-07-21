###
# AJAX call for main info page.
###

# Set-timeout values: current, min/max limits and adjustment coefficient.
set_timeout_cur = 500
set_timeout_max = 1000
set_timeout_min = 0
set_timeout_mod = 25

# Previous image timestamp, used to detect whether
# a new image is available.
prev_image_tstamp = null

info = ->
    ###
    # Make the AJAX server info request.
    ###

    # Mark the time-of-request.
    request_time = new Date()
    
    $.ajax 'service/info',
        dataType : 'json'
        cache    : false
        timeout  : 2000
        success  : (data) ->

            # Update the AJAX response time. 
            now = new Date()
            elapsed = (now.getTime() - request_time.getTime()) / 1000;
            $('#response_time').text elapsed.toFixed(3)

            short_tstamp = data.latest_tstamp.slice(0, -7)  # Trim off ms.
            short_tstamp = short_tstamp.substring(11)  # Trim off date.
            $('#latest_tstamp_hud').text short_tstamp
            $('#server_time').text data.server_time
            $('#load_avg').text data.load_avg
            $('#db_size').text data.db_size
            $('#latest_tstamp').text data.latest_tstamp.slice(0, -3)
            $('#set_timeout').text (set_timeout_cur/1000).toFixed(3)

            # If the database is empty, turn OFF live display
            # and try fetching info again.
            if data.db_size == '0'
                $('#live_view').css 'display', 'none'
                tryInfoAgain()
                
            # Otherwise, if a new image arrived, set the <img> src attribute
            # (and make sure live display is ON.)
            else if prev_image_tstamp != data.latest_tstamp
                $('#latest_image').attr 'src', data.latest_url
                $('#live_view').css 'display', 'block'
                prev_image_tstamp = data.latest_tstamp

            # Otherwise, the database is not empty but there is no
            # newer image available. So try fetching info again.
            else
                tryInfoAgain()
                
        error : (data) ->
            
            # Update the AJAX response time. 
            now = new Date()
            elapsed = (now.getTime() - request_time.getTime()) / 1000;
            $('#response_time').text elapsed.toFixed(3)

            $('#server_time').text 'Error'
            $('#load_avg').text ''
            $('#db_size').text ''
            $('#latest_tstamp').text ''
            $('#set_timeout').text (set_timeout_cur/1000).toFixed(3)
            tryInfoAgain()


tryInfoAgain = ->
    ###
    # Increase the set-timeout delay, and then
    # set info() as the timeout callback.
    ###
    if set_timeout_cur < set_timeout_max
        set_timeout_cur += set_timeout_mod
    callback = -> info 0
    setTimeout callback, set_timeout_cur

    
onImageLoad = ->
    ###
    # Decrease the set-timeout delay and call info().
    ###
    if set_timeout_cur > set_timeout_min
        set_timeout_cur -= set_timeout_mod
    info()


# Only run when document has loaded
$ ->
    info()

# All CoffeeScript output is wrapped in an anonymous function,
# so in order to use functions as top-level variables (like in HTML)
# let's attach them as properties on *window*.
window.wabbitOnImageLoad = onImageLoad

# End of file.
