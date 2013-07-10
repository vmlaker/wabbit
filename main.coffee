###
# Wabbit AJAX.
###

timeout = 250

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
                $('#last_tstamp').text data.last_tstamp
                $('#last_url').text data.last_url
                $('#timeout').text timeout
                $('#last_image').attr 'src', data.last_url
                if timeout > 250
                        timeout -= 10
                callback = -> info 0
                setTimeout callback, timeout
        error    : (data) ->
                $('#server_time').text 'Error'
                $('#db_size').text 'Error'
                $('#last_tstamp').text 'Error'
                $('#last_url').text 'Error'
                $('#timeout').text timeout
                timeout += 10
                callback = -> info 0
                setTimeout callback, timeout
    
main = ->
    ###
    # Main script entry point.
    ###
    info()

# Only run when document has loaded
$ ->
    main()
