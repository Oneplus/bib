Save bib in browser to Github repo
==================================

![screenshot](https://raw.github.com/Oneplus/bib/master/screenshot.jpg)

### News

Now, you can install this script from userscript, [install](http://userscripts.org/scripts/show/293624)!

### Usage

You can deploy `bibsaver.js` to your greasemonkey.

Firstly, you need to create a repo and push a file `db.bib` into it.
Then config the script with
```
var username = "Oneplus";
var password = "password";
var reponame = "bib";
var branchname = "experimental"; 
```

Then, whenever it detect some website provided bib file, it will add a button at the tail of the page.
When the button clicked, it will save the bib file to your specified github repo.

Currently configured bib source is [aclweb.org](aclweb.org) and [scholar.google.com](scholar.google.com).
Surely you can add other sources by add an entry to the script header.

### changelog

#### 2014-02-06 0.0.3

* [FIX] fix bug issue from illegal entry
* [ADD] add this script to userscript.org

#### 2014-01-29 0.0.2

* [ADD] we have a button.
* [ADD] we also have the redundancy check, you will not be afraid of the double-added entries.

#### 2013-12-26 0.0.1

* [ADD] First version of the project.