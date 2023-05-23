// Bypasses login page for testing/viewing purposes
const username = 'portfolio';
const password = 'sitevisitor';

document.getElementById("bypass").addEventListener("click", function() {
    document.getElementById("id_username").value = username;
    document.getElementById("id_password").value = password;
});