function sendToken() {
    const params = document.location.hash.slice(1);
    const tokenRequest = new XMLHttpRequest();
    tokenRequest.addEventListener("load", requestComplete);
    tokenRequest.addEventListener("error", requestFailed);
    tokenRequest.addEventListener("abort", requestCanceled);
    tokenRequest.open("POST", "http://localhost:5000/token");
    tokenRequest.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    tokenRequest.send(params);
};

function requestComplete() {
    document.body.innerHTML = "Sent token to app. You may close this window now. :)";
};

function requestFailed() {
    document.body.innerHTML = "Sending of token to app failed. Please restart the app and try again. :(";
};

function requestCanceled() {
    document.body.innerHTML = "Sending of token to app cancelled. Please restart the app and try again. :(";
};