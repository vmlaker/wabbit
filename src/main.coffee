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
            $('#server_time').text data.server_time
            $('#db_size').text data.db_size
            $('#last_tstamp').text data.last_tstamp.slice(0, -7)  # Trim off ms.
            $('#timeout').text tout_cur

            # If a new image arrived, set the <img> src attribute,
            # otherwise call info() again in a timeout.
            if prev_tstamp != data.last_tstamp
                $('#last_image').attr 'src', data.last_url
                prev_tstamp = data.last_tstamp
            else
                tryInfoAgain()            
        error : (data) ->
            $('#server_time').text 'Error'
            $('#db_size').text ''
            $('#last_tstamp').text ''
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
    $('#last_image').on('load', onImageLoad)
    info()

# Only run when document has loaded
$ ->
    main()
