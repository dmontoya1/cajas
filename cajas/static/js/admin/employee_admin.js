(function($) {
    $(document).ready(function(){

        $('#id_charge').change(function(){
            cargo = $(this).val()
            if(cargo == '4' || cargo == '6'){
                $(".field-office").show();
                $(".field-office_country").hide();
            }
            else if(cargo == '5'||  cargo == '7' || cargo == '8'|| cargo == '9') {
                $(".field-office_country").show();
                $(".field-office").hide();
            }
        })
        if ($('#id_charge').val() == 4 || $('#id_charge').val() == 6){
            $(".field-office").show();
            $(".field-office_country").hide();
        }
        else{
            $(".field-office").hide();
            $(".field-office_country").show();
        }
        console.log($('#id_charge').val())
    });
})(django.jQuery);
