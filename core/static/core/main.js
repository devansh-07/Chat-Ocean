function loadSearchForm () {
	var xhr = new XMLHttpRequest();
	// OPEN - type, url/file, bool async
	xhr.open('GET', '/_searchContact', true);

	xhr.onload = function(){
		if (this.status == 200){
			document.getElementById("sideContent").innerHTML = xhr.responseText;
		}
	}

	xhr.send();
}

function loadChats () {
	var xhr = new XMLHttpRequest();
	xhr.open('GET', '/_loadChats', true);

	xhr.onload = function(){
		if (this.status == 200){
			document.getElementById("sideContent").innerHTML = xhr.responseText;
		}
	}

	xhr.send();
}

function searchUser() {
	var uname = document.getElementById("searchUsername").value;
	var data = new FormData();
	data.append('username', uname);

	var xhr = new XMLHttpRequest();
	xhr.open('POST', '/searchUser', true);

	xhr.onload = function(){
		if (this.status == 200){
			document.getElementById("searchResults").innerHTML = xhr.responseText;
		}
	}

	xhr.send(data);
}

function loadRequests() {
	var xhr = new XMLHttpRequest();
	xhr.open('GET', '/loadRequests', true);

	xhr.onload = function(){
		if (this.status == 200){
			document.getElementById("sideContent").innerHTML = xhr.responseText;
		}
	}

	xhr.send();
}

function loadSearchFormUtil () {
	chatsBtn.className = "";
	requestsBtn.className = "";
	contactBtn.className = "active";
	loadSearchForm();
}

function loadChatsUtil() {
	contactBtn.className = "";
	requestsBtn.className = "";
	chatsBtn.className = "active";
	loadChats();
}

function loadRequestsUtil() {
	contactBtn.className = "";
	chatsBtn.className = "";
	requestsBtn.className = "active";
	loadRequests();
}

function send_friend_request(username) {
	var data = new FormData();
	data.append('username', username);

	var xhr = new XMLHttpRequest();
	xhr.open('POST', '/sendRequest', true);

	xhr.onload = function(){
		if (this.status == 200) {
			var vectors = document.getElementById("addFriend");
			vectors.className = "fa fa-check";
		}
	}

	xhr.send(data);
}

function toggleSentRequestList() {
	$("#sentRequestList").toggleClass("d-none");
};

function toggleReceivedRequestList() {
	$("#receivedRequestList").toggleClass("d-none");
};

function _removeSentRequest(username) {
	var data = new FormData();
	data.append('username', username);

	var xhr = new XMLHttpRequest();
	xhr.open('POST', '/removeSentRequest', true);

	xhr.onload = function() {
		if (this.status == 200) {
			loadRequests();
		}
	}

	xhr.send(data);
}

function _removeReceivedRequest(username) {
	var data = new FormData();
	data.append('username', username);

	var xhr = new XMLHttpRequest();
	xhr.open('POST', '/removeReceivedRequest', true);

	xhr.onload = function() {
		if (this.status == 200) {
			loadRequests();
		}
	}

	xhr.send(data);
}

function _acceptReceivedRequest(username) {
	var data = new FormData();
	data.append('username', username);

	var xhr = new XMLHttpRequest();
	xhr.open('POST', '/acceptReceivedRequest', true);

	xhr.onload = function() {
		if (this.status == 200) {
			loadRequests();
		}
	}

	xhr.send(data);
}

function toggleProfile() {
	$("#Profile").toggleClass("d-none");
}

var contactBtn = document.querySelector("#addcontact");
var chatsBtn = document.querySelector("#mychats");
var requestsBtn = document.querySelector("#allrequests");

contactBtn.onclick = loadSearchFormUtil;
chatsBtn.onclick = loadChatsUtil;
requestsBtn.onclick = loadRequestsUtil;

loadChatsUtil();
