(function($) {
    $(document).ready(function(){
        $(".field-crossover_type").hide();
        $(".field-counterpart").hide();
        $(".field-relationship").hide();

        $('#id_concept_type').change(function(){
            type = $(this).val()
            if(type == "SM"){
                $(".field-crossover_type").hide();
                $(".field-counterpart").hide();
                $(".field-relationship").hide();
            }
            else {
                $(".field-crossover_type").show();
                $(".field-counterpart").show();
                $(".field-relationship").show();
            }
        })
    });
})(django.jQuery);
