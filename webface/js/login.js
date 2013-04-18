$(function(){
    $('#tab_login').on('click', function(){
        $('#tab_register').parent().removeClass('active');
        $(this).parent().addClass('active');

        $('#form_login').show();
        $('#form_register').hide();
    });

    $('#tab_register').on('click', function(){
        $('#tab_login').parent().removeClass('active');
        $(this).parent().addClass('active');

        $('#form_register').show();
        $('#form_login').hide();
    });
});
