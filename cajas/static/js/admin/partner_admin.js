(function($) {
    $(document).ready(function(){
        $(".field-direct_partner").hide();
        if ($('#id_partner_type').val() == 'DIR'){
            $(".field-direct_partner").hide();
        }
        $('#id_partner_type').change(function(){
        // hidding campos del formulario
        
            if($(this).val() == 'DIR'){
                // Si el usuario es un Coordinador de Institucion
                $(".field-direct_partner").hide();
            }
            else if($(this).val() == 'INDIR'){
                // Si el usuario es conductor
                $(".field-direct_partner").show();
            }
            else {
                $(".field-direct_partner").hide();
            }
        })
    });
})(django.jQuery);