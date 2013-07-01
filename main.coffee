###
# Wabbit AJAX.
###

info = ->
    ###
    # Make the AJAX server info request.
    ###

    $.ajax '/info',
        dataType : 'json'
        cache    : false
        timeout  : 1000
        success  : (data) ->
                $('#server_time').text data.server_time
                $('#db_size').text data.db_size
                callback = -> info 0
                setTimeout callback, 250
        error    : (data) ->
                $('#server_time').text 'Error'
                $('#db_size').text 'Error'
                callback = -> info 0
                setTimeout callback, 250
    
main = ->
    ###
    # Main script entry point.
    ###
    info()

# Only run when document has loaded
$ ->
    main()
