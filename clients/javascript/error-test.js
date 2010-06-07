// $Id$
// Copyright ClearWind Consulting Ltd., 2008-9
// Version 1.2
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
    form.setAttribute("action", host + "www.clearwind.ca/v/1/"); 
    form.setAttribute("method", "post");

    var now = new Date;

    arecibo.addInput(form, iframe, "account", arecibo.account);
    arecibo.addInput(form, iframe, "server", arecibo.server);
    arecibo.addTextArea(form, iframe, "msg", arecibo.msg);
    arecibo.addInput(form, iframe, "status", arecibo.status);
    arecibo.addInput(form, iframe, "priority", arecibo.priority);
    arecibo.addInput(form, iframe, "uid", arecibo.uid);
    arecibo.addInput(form, iframe, "username", arecibo.uid);
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
