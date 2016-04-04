var soccer_pics = [
	"http://localhost:16080/static/images/liverpool.png",
	"http://localhost:16080/static/images/coutinho.jpg",
	"http://localhost:16080/static/images/sturridge.gif"
];

var soccer_captions = [
	"liverpool pic",
	"phillipe coutinho",
	"daniel sturridge"
];

var theater_pics = [
	"http://localhost:16080/static/images/romeo_and_juliet.jpg", 
	"http://localhost:16080/static/images/uoam_king_jester_and_i.jpg", 
	"http://localhost:16080/static/images/ouam_group.jpg",
	"http://localhost:16080/static/images/pyongyang_style.jpg", 
	"http://localhost:16080/static/images/picasso.jpg",
	"http://localhost:16080/static/images/picasso_rehearsal_group.jpg", 
	"http://localhost:16080/static/images/picasso_group.jpg"
];

var theater_captions = [
	"romeo and juliet cast",
	"the king, jester, and i",
	"Once Upon a Mattress group pic",
	"pyongyang style pic",
	"picasso at the lapin agile poster",
	"picasso rehearsal pic",
	"picasso production pic"
];

var policy_pics = [
	"http://localhost:16080/static/images/mndi_paul.jpg",
	"http://localhost:16080/static/images/mndi_arthur.jpg", 
	"http://localhost:16080/static/images/mndi_debate.jpg", 
	"http://localhost:16080/static/images/debate_ketchup_arthur.jpg" 
];

var policy_captions = [
	"wilson and paul at MNDI",
	"wilson and arthur at MNDI",
	"oakwood debate at MNDI",
	"wilson, katja, and arthur"
];

var acadec_pics = [
	"http://localhost:16080/static/images/acadec_captains.jpg", 
	"http://localhost:16080/static/images/ties_are_cool.jpg",
	"http://localhost:16080/static/images/acadec_nats_2013.jpg"
];

var acadec_captions = [
	"acadec captains: herb, wilson, cliff",
	"tyler, josh, wilson in ties",
	"2013 nats winning team"
];

var dict_pics = {
	"soccer": soccer_pics,
	"theater": theater_pics,
	"policy": policy_pics,
	"acadec": acadec_pics
};

var dict_captions = {
	"soccer": soccer_captions,
	"theater": theater_captions,
	"policy": policy_captions,
	"acadec": acadec_captions
};

// returns index where string is found in container
function find_index(str, container) {
	for (i = 0; i < container.length; i++) {
		if (container[i] === str) {
			return i;
		}
	}
	return -1;
}

function getter(prev_or_next, term) {
	var pic = document.getElementById(term);
	var idx = find_index(pic.src, dict_pics[term]);
	if (prev_or_next === "prev") {
		if (idx <= 0) {
			pic.setAttribute("src", dict_pics[term][0]);
			pic.setAttribute("alt", dict_captions[term][0]);
		}
		else {
			pic.setAttribute("src", dict_pics[term][idx - 1]);
			pic.setAttribute("alt", dict_pics[term][idx - 1]);
		}
	}
	else {		//next
		if (idx == dict_pics[term].length - 1) {
			pic.setAttribute("src", dict_pics[term][idx]);
			pic.setAttribute("alt", dict_pics[term][idx]);
		}
		else {
			pic.setAttribute("src", dict_pics[term][idx + 1]);
			pic.setAttribute("alt", dict_pics[term][idx + 1]);
		}
	}
	return;
}

window.onload = function() {
	document.getElementsByClassName("active").className = "";
	document.getElementById("interests").className = "active";
};
document.getElementById("soccer_prev").onclick= function() {
	getter("prev", "soccer");
	return false;
};
document.getElementById("soccer_next").onclick= function() {
	getter("next", "soccer");
	return false;
};
document.getElementById("theater_prev").onclick= function () {
	getter("prev", "theater");
	return false;
};
document.getElementById("theater_next").onclick= function() {
	getter("next", "theater");
	return false;
};
document.getElementById("policy_prev").onclick= function() {
	getter("prev", "policy");
	return false;
};
document.getElementById("policy_next").onclick= function() {
	getter("next", "policy");
	return false;
};
document.getElementById("acadec_prev").onclick= function() {
	getter("prev", "acadec");
	return false;
};
document.getElementById("acadec_next").onclick= function() {
	getter("next", "acadec");
	return false;
};
