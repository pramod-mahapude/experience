jQuery( document ).ready(function() {

jQuery(document).on("blur",".cname", function(){
	var text = this.value;
	text = text.toLowerCase();

	//text.substr(0,1).toUpperCase()+text.substr(1);
    text = text.charAt(0).toUpperCase() + text.slice(1);
	jQuery(this).val(text);

	});

jQuery(document).on("keypress",".onlynumeric", function(e){
	if (e.which != 8 && e.which != 0 && (e.which < 48 || e.which > 57)) {
			/* display error message */
			// jQuery("#errmsg").html("Digits
			// Only").show().fadeOut("slow");
			return false;
		}
});
});
