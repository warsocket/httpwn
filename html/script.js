function sizeConsole(){
	var text = getConsole();
	var t = text.getBoundingClientRect().top
	var newHeight = Math.max( window.innerHeight - t - 12, 100)
	text.style.height =  newHeight + "px";
}

function getConsole(){
	return document.getElementsByClassName("console")[0];
}

function getConsoleText(){
	return getConsole().value;
}

function writeConsoleText(text){
	getConsole().value = text;
}

writeConsoleText("");
sizeConsole()
window.addEventListener("resize", sizeConsole)


//Now client side functions:
function toHex(text)
{
    var newText = "";
    for(var i in text)
    {
        var newCode = text.charCodeAt(i).toString(16);
        if (newCode.length < 2) newCode = "0" + newCode;
        newText += newCode;
    }

    return newText;
}

function fromHex(text)
{
    var newText = "";
    for(i = 0; i < text.length; i += 2)
    {
        newText += String.fromCharCode( parseInt(text.substring(i,i+2), 16) );
    }

    return newText;
}

function mapContent(f){
	writeConsoleText(f(getConsoleText()));
}


//MY ip endpoint functions
       
async function writeapi(url){
    var c = document.getElementById("console");
    const r = await fetch(url);
    c.value = await r.text();
};

//now we map eevent listeners
document.getElementById("ue").addEventListener("click", () => mapContent(encodeURIComponent));
document.getElementById("ud").addEventListener("click", () => mapContent(decodeURIComponent));
document.getElementById("be").addEventListener("click", () => mapContent(window.btoa));
document.getElementById("bd").addEventListener("click", () => mapContent(window.atob));
document.getElementById("he").addEventListener("click", () => mapContent(toHex));
document.getElementById("hd").addEventListener("click", () => mapContent(fromHex));

document.getElementById("myip").addEventListener("click", () => writeapi('/api/myip'));
document.getElementById("myipv4").addEventListener("click", () => writeapi(window.location.protocol + '//ipv4.httpwn.org/api/myip'));
document.getElementById("myipv6").addEventListener("click", () => writeapi(window.location.protocol + '//ipv6.httpwn.org/api/myip'));
