/* function replaceNav(mql) {
	if (mql.matches) {
		var nav = document.getElementById("nav");
		var new_nav = '<nav id="desktop">\
			<ul class="nav nav-pills nav-stacked" role="navigation">\
				<li role="presentation" class="active"><a href="/">Home</a></li>\
				<li role="presentation"><a href="/work">Work Experience</a></li>\
				<li role="presentation"><a href="/interests">Interests</a></li>\
				<li role="presentation"><a href="/skills">Skills</a></li>\
				<li role="presentation"><a href="/user">Creae Account</a></li>\
				<li role="presentation"><a href="/login">Login</a></li>\
			</ul>\
		</nav>';
	nav.innerHTML = new_nav;
	}
	return;
}

var mql = window.matchMedia("screen and (min-device-width: 1200px)");
replaceNav(mql);
mql.addListener(replaceNav); */
//change active
$(document).ready(function () {
    $.each($('#navbar').find('li'), function() {
        $(this).toggleClass('active',
            $(this).find('a').attr('href') == window.location.pathname);
    });
});