document.getElementsByClassName("include_system_calls")[0].innerHTML=`<div>
      <input type="checkbox" id="include_system_calls_id" name="Include System Calls"
             >
      <label for="systemCalls">Include System Calls</label>
    </div>`

    function systemCalls(){
    let checkbox = document.getElementById('include_system_calls_id');
    if (checkbox.checked == false) {
	   document.getElementById("obp_app_table").style.display = "none";
    }else{
	    document.getElementById("obp_app_table").style.display = "";
    }
}