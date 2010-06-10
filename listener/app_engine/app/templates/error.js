// $Id$
// Copyright ClearWind Consulting Ltd., 2008-10
// Version 1.3
// Posts to /v/1/

var arecibo = new Object();
arecibo.loaded = false;

arecibo.register = function(elem, event, func) {
    if (elem.addEventListener) {
        elem.addEventListener(event, func, false);
        return true;
    } else if (elem.attachEvent) {
        var result = elem.attachEvent("on"+event, func);
        return result;
    }
    return false;
};

arecibo.addInput = function(form, doc, name, value) {
    if (typeof(value) == "undefined") {
        return;
    }
    var tmp = doc.createElement("input");
    tmp.setAttribute("type", "text");
    tmp.setAttribute("name", name);
    tmp.setAttribute("value", value);
    form.appendChild(tmp);
};

arecibo.addTextArea = function(form, doc, name, value) {
    if (typeof(value) == "undefined") {
        return;
    }
    var tmp = doc.createElement("textarea");
    tmp.setAttribute("type", "text");
    tmp.setAttribute("name", name);
    tmp.innerHTML = value;
    form.appendChild(tmp);
};

arecibo.createForm = function() {
    try {
        var iframe = window.frames.error.document;
    } catch(e) {
        return;
    }
    if (arecibo.loaded) { return; }
    arecibo.loaded = true;
    var form = iframe.createElement("form");
    var host = (("https:" == document.location.protocol) ? "https://" : "http://");
    form.setAttribute("action", host + "{{ domain }}/v/1/");
    form.setAttribute("method", "post");

    var now = new Date;

    arecibo.addInput(form, iframe, "account", arecibo.account);
    arecibo.addInput(form, iframe, "server", arecibo.server);
    arecibo.addTextArea(form, iframe, "msg", arecibo.msg);
    arecibo.addInput(form, iframe, "status", arecibo.status);
    arecibo.addInput(form, iframe, "priority", arecibo.priority);
    arecibo.addInput(form, iframe, "uid", arecibo.uid);
    arecibo.addInput(form, iframe, "username", arecibo.username);
    arecibo.addInput(form, iframe, "timestamp", now.toUTCString());
    if (typeof(arecibo.url) == "undefined") {
        arecibo.addInput(form, iframe, "url", window.location);
    } else {
        arecibo.addInput(form, iframe, "url", arecibo.url);
    }
    arecibo.addInput(form, iframe, "type", arecibo.type);
    arecibo.addTextArea(form, iframe, "traceback", arecibo.traceback);
    arecibo.addTextArea(form, iframe, "request", arecibo.request);

    iframe.body.appendChild(form);
    form.submit();
};

arecibo.postLoad = function() {
    var iframe = document.createElement("iframe");
    iframe.name = "error";
    iframe.id = "error";
    // if you want to see what's going on, uncomment the next line
    iframe.style.visibility = "hidden";
    arecibo.register(iframe, "load", arecibo.createForm);
    document.body.appendChild(iframe);
};

arecibo.run = function() {
    arecibo.register(window, "load", arecibo.postLoad);
};

arecibo.recordException = function(e) {
    arecibo.msg = e.toString();
    arecibo.type = e.name;

    var line;

    if (e.line) { // WebKit
        line = e.line;
    } else if (e.lineNumber) { // Mozilla
        line = e.lineNumber;
    }

    if (e.sourceURL) { // Webkit
        arecibo.url = e.sourceURL;
    } else if (e.fileName) { // Mozilla
        arecibo.url = e.fileName;
    } else {
        arecibo.url = window.location;
    }

    if (line) {
        arecibo.msg = arecibo.url + " line " + line + ": " + arecibo.msg;
    }

    // Currently Mozilla only:
    if (e.stack) arecibo.traceback = e.stack;

    arecibo.postLoad();
};

arecibo.registerGlobalHandler = function() {
    /*
        NOTE: Currently this will only work on Firefox and Internet Explorer.

        Safari and Chrome have open feature requests for global error handlers:

        https://bugs.webkit.org/show_bug.cgi?id=8519
        http://code.google.com/p/chromium/issues/detail?id=7771
    */

    window.onerror = function(msg, url, ln, stack) {
        arecibo.msg = url + " at line " + ln + ": " + msg;
        arecibo.traceback = stack; // NOTE: This will only be available on Firefox
        arecibo.url = url;

        arecibo.postLoad();
    };
};
