$(function(){
    $('#tab_logs').on('click', function(){
        $('#tab_users').parent().removeClass('active');
        $(this).parent().addClass('active');

        $('#logs').show();
        $('#users').hide();
    });

    $('#tab_users').on('click', function(){
        $('#tab_logs').parent().removeClass('active');
        $(this).parent().addClass('active');

        $('#users').show();
        $('#logs').hide();
    });
});
