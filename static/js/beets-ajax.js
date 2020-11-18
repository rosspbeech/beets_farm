$(document).ready(function() {


    $('#new_sound').click(function(){
        var beetIdVar;
        beetIdVar = $(this).attr('data-beetid');

        $.get('/beets/new_sound/',
        {beetid:beetIdVar},
        function(data) {
            $('#song').attr('src', data['src']);
            $('#song-title').html("This is: " + data['name']);
            $('#song').css("display", "block");
            $('#song-holder').css("display", "block")
            $('#song-artist').html("By the wonderful: " + data['artist'])
            $('#song')[0].play();
            $('#new_sound').attr('data-beetid', data['bid'])
        })
    });
});