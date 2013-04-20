$(function(){
    $('#tab_logs').on('click', function(){
        $('#tab_users').parent().removeClass('active');
        $(this).parent().addClass('active');

        $('#table_logs').show();
        $('#table_users').hide();
    });

    $('#tab_users').on('click', function(){
        $('#tab_logs').parent().removeClass('active');
        $(this).parent().addClass('active');

        $('#table_users').show();
        $('#table_logs').hide();
    });
});
