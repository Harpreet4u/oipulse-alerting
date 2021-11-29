// ==UserScript==
// @name         OSPL
// @namespace    http://tampermonkey.net/
// @require http://code.jquery.com/jquery-latest.js
// @match        https://www.oipulse.com/app/advance-chart
// @Version 1
// @grant none
// ==/UserScript==

(() => {
    let interval;
    $(document).ready(function(){
        const btn = document.createElement("Button");
        btn.innerHTML = "Start";
        btn.id = "ospl";
        btn.style.position = "absolute";
        btn.style.top = 0;
        btn.style.left = 0;
        btn.style.zIndex = 1000;
        btn.onclick = function() {
            if (interval) {
                console.log("cancelling interval");
                clearInterval(interval);
                interval = null;
                $("#ospl").html("Start");
                return;
            }
           $("#ospl").html("Stop");
           interval = setInterval(callback, 4000)
        }
       document.body.appendChild(btn);
    })

})()

function callback() {
    const i = $("iframe");
    let imageDataUrl;
    if (i) {
        imageDataUrl = i[0].contentWindow.document.getElementsByTagName("canvas")[0].toDataURL();
    }
    else {
        const canvas = $("canvas");
        if (canvas) {
           imageDataUrl = canvas[0].toDataURL();
        }
    }
    if (imageDataUrl) {
        var a = document.createElement("a");
        a.href = "data:text," + imageDataUrl;   //content
        a.download = "ospl_image.txt";            //file name
        a.click();
    }

}