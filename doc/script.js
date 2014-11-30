/***************************************************/
/*                                                 */
/*  JavaScript file for Wabbit documentation.      */
/*                                                 */
/***************************************************/

/**
   Upon document load, set callbacks
   and process the hash.
*/
$(document).ready(function(){

    $('#btnInstall').click(function(){
        select('#btnInstall');
        $('#content').load('install.html');
    });

    $('#btnFAQ').click(function(){
        select('#btnFAQ');
        $('#content').load('faq.html');
    });

    $('#btnAbout').click(function(){
        select('#btnAbout');
        $('#content').load('about.html');
    });
    $(window).on('hashchange', onHashChange);
    onHashChange();
});

/**
   Perform button click based on window URL hash.
*/
function onHashChange(){
    var hash2click = {}
    hash2click['#install'] = '#btnInstall';
    hash2click['#faq'] = '#btnFAQ';
    hash2click['#about'] = '#btnAbout';
    var hash = $(location).attr('hash');
    var click = hash2click[hash];
    if (!click) {
        click = '#btnInstall';
    }
    $(click).click();
}

/**
   Set the class for button, based on hash.
*/
var buttons = ['#btnInstall', '#btnFAQ', '#btnAbout'];
function select(button){
    for (ii=0; ii<buttons.length; ii++) {
        if (buttons[ii] == button) {
            $(buttons[ii]).attr('class', 'navitemselected');
        }else{
            $(buttons[ii]).attr('class', 'navitem');
        }
    }
}
