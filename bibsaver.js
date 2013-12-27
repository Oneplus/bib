// ==UserScript==
// @name        bibsaver
// @namespace   http://oneplus.info
// @include     http://aclweb.org/anthology/*.bib
// @description With this script, you are allowed to save bib to a github repo.
// @version     0.0.1
// @require     http://code.jquery.com/jquery-1.10.2.min.js
// @require     https://raw.github.com/michael/github/master/lib/base64.js
// @require     https://raw.github.com/michael/github/master/lib/underscore-min.js
// @require     https://raw.github.com/michael/github/master/github.js
// @grant       none
// ==/UserScript==

var save = confirm("Save this bib to repo?");

if (!save)
    exit(1);

var username = "Oneplus";
var password = "passwordissensitive";
var reponame = "bib";
var branchname = "experimental";

var bibElement = document.getElementsByTagName('pre')[0];
var bibText = bibElement.innerHTML;

var github = new Github({
  username: username,
  password: password
});

var repo = github.getRepo(username, reponame);

var sha = null;
var content = null;

$.get(
    "https://api.github.com/repos/" + username + "/" + reponame + "/git/refs/heads/" + branchname,
    function(data) {
        console.log(data.object.sha);
        sha = data.object.sha;
        $.get(
            "https://api.github.com/repos/" + username + "/" + reponame + "/contents/db.bib?ref=" + branchname,
            function(data) {
                console.log( data.content );
                content = Base64.decode( data.content );
                console.log(content);

                repo.write("experimental", 
                           "db.bib",
                           bibText + "\n" + content,
                           "bib from : " + window.location.href,
                           function(err) {
                    alert(err);
                });
            });
    });
