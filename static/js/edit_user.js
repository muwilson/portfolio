window.onload = function() {
	document.getElementsByClassName("active").className = "";
	document.getElementById("edit user").className = "active";
};
function check_pwd() {
	var new_pw = document.getElementsByName("new_pw")[0];
	var old_pw = document.getElementsByName("old_pw")[0];
	if (new_pw === old_pw) {
		return true;
	}
	else {
		document.getElementById("pw_error").innerHTML = "new passwords do not match";
		return false;
	}
}
document.getElementById("submit").onclick= function() {
	return check_pwd();
};