/***************************************************/
/*                                                 */
/*  JavaScript file for Wabbit documentation.      */
/*                                                 */
/***************************************************/

/*  Setup mappings of hashtags --> buttons and
 *  buttons --> contents.
 */
var hashes = ['#install', '#faq', '#about'];
var buttons = ['#btnInstall', '#btnFAQ', '#btnAbout'];
var contents = ['#contentInstall', '#contentFAQ', '#contentAbout'];
var hash2button = {}
for (ii=0; ii<hashes.length; ii++){
    hash2button[hashes[ii]] = buttons[ii];
}
var button2content = {}
for (ii=0; ii<buttons.length; ii++){
    button2content[buttons[ii]] = contents[ii];
}

/*
 *  Upon document load...
 */
$(document).ready(function(){

    /* Set the click() callbacks. */
    for(ii=0; ii<buttons.length; ii++){
        button = buttons[ii];
        content = contents[ii];
        /*  Set the callbacks, and deal with JavaScript closures
         *  by returning a functions, and immediately calling the callback.
         */
        $(button).click(function(button, content){
            return function(){ 
                select(button);
                $('#content').load('index.html ' + content);
            }
        }(button, content));  // Immediately call.
    }

    /* Set the hashChange event. */
    $(window).on('hashchange', onHashChange);

    /*  The default landing hashtag is #install. 
     *  Set it to the default value in case it's not present,
     *  or it is an illegal value.
     */
    if (!window.location.hash || hashes.indexOf(window.location.hash) == -1){
        window.location.hash = '#install';
    }

    /* Go ahead and initally call the hashChange callback. */
    onHashChange();
});

/*
 *  Set the class for button, based on hashtag.
 */
function select(button){
    for (ii=0; ii<buttons.length; ii++) {
        if (buttons[ii] == button) {
            $(buttons[ii]).attr('class', 'navitemselected');
        }else{
            $(buttons[ii]).attr('class', 'navitem');
        }
    }
}

/*
 *  Retrieve the button based on current hashtag,
 *  and click it.
 */
function onHashChange(){
    var button = hash2button[window.location.hash];
    if (!button) {
         return;
    }
    $(button).click();
}
