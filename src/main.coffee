###
# AJAX call for main info page.
###

# Timeout value, min/max limits and adjustment coefficient.
tout_cur = 500
tout_max = 1000
tout_min = 0
tout_mod = 25

# Previous timestamp, used to detect whether a new image
# is available.
prev_tstamp = null

info = ->
    ###
    # Make the AJAX server info request.
    ###
    $.ajax 'service/info',
        dataType : 'json'
        cache    : false
        timeout  : 2000
        success  : (data) ->
            short_tstamp = data.latest_tstamp.slice(0, -7)  # Trim off ms.
            short_tstamp = short_tstamp.substring(11)  # Trim off date.
            $('#latest_tstamp_hud').text short_tstamp
            $('#server_time').text data.server_time
            $('#db_size').text data.db_size
            $('#latest_tstamp').text data.latest_tstamp
            $('#timeout').text tout_cur

            # If the database is empty, turn OFF live display
            # and try fetching info again.
            if data.db_size == "0"
                $('#live_view').css 'display', 'none'
                tryInfoAgain()
                
            # Otherwise, if a new image arrived, set the <img> src attribute
            # (and make sure live display is ON.)
            else if prev_tstamp != data.latest_tstamp
                $('#latest_image').attr 'src', data.latest_url
                $('#live_view').css 'display', 'block'
                prev_tstamp = data.latest_tstamp

            # Otherwise, the database is not empty but there is no
            # newer image available. So try fetching info again.
            else
                tryInfoAgain()
                
        error : (data) ->
            $('#server_time').text 'Error'
            $('#db_size').text ''
            $('#latest_tstamp').text ''
            $('#timeout').text tout_cur
            tryInfoAgain()


tryInfoAgain = ->
    ###
    # Increase the timeout delay, and then
    # set info() as the timeout callback.
    ###
    if tout_cur < tout_max
        tout_cur += tout_mod
    callback = -> info 0
    setTimeout callback, tout_cur

    
onImageLoad = ->
    ###
    # Set timeout on info().
    ###
    if tout_cur > tout_min
        tout_cur -= tout_mod
    callback = -> info 0
    setTimeout callback, tout_cur


main = ->
    ###
    # Main script entry point.
    ###
    $('#latest_image').on('load', onImageLoad)
    info()

# Only run when document has loaded
$ ->
    main()
