(function($) {
    $(document).ready(function(){
        $(".field-office").hide();
        $(".field-office_country").hide();

        $('#id_charge').change(function(){
            cargo = $(this).val()
            if(cargo == '4' || cargo == '5'|| cargo == '6'){
                // Si el usuario es un Coordinador de Institucion
                $(".field-office").show();
                $(".field-office_country").hide();
            }
            else if(cargo == '7' || cargo == '8'|| cargo == '9') {
                // Si el usuario es conductor
                $(".field-office_country").show();
                $(".field-office").hide();
            }
        })
    });
})(django.jQuery);
