//Service Worker installation
if ('serviceWorker' in navigator) navigator.serviceWorker.register('./sw.js')

var https = location.protocol == "https:"

//PWA install prompt
window.addEventListener('beforeinstallprompt', (e) => {

	e.preventDefault()
	deferredPrompt = e

	install.classList.remove("hidden")
	install.addEventListener('click', () => {
		install.disabled = true
		e.prompt()
	})
    
});


function writearray(array, firstnode){
	let first = true
	for (var item of array){
		if (!first){
			let emptyspan = document.createElement("span")
			let span = document.createElement("span")
			span.innerText = item
			if(https){
				span.classList.add("https")
			}else{
				span.classList.add("http")
			}
			document.body.appendChild(emptyspan)
			document.body.appendChild(span)		
		}else{
			firstnode.innerText = item
		}

		first = false
	}
}

if (https){
	protoswitch.innerText = "Using HTTPS"
	protoswitch.className = "https"
	protoswitch.addEventListener('click', () => document.location.href = "http:" + document.location.href.substring(document.location.protocol.length))
	for (span of document.getElementsByTagName("SPAN")) span.classList.add("https")
}else{
	protoswitch.innerText = "Using HTTP"
	protoswitch.className = "http"
	protoswitch.addEventListener('click', () => document.location.href = "https:" + document.location.href.substring(document.location.protocol.length))
	for (span of document.getElementsByTagName("SPAN")) span.classList.add("http")
}





fetch("/ip", options={mode: "cors"}).then((r) => r.text()).then((t) => ip.innerText = t).catch(() => ip.innerText = "-")
fetch("//ipv4.httpwn.org/ip", options={mode: "cors"}).then((r) => r.text()).then((t) => ipv4.innerText = t).catch(() => ipv4.innerText = "-")
fetch("//ipv6.httpwn.org/ip", options={mode: "cors"}).then((r) => r.text()).then((t) => ipv6.innerText = t).catch(() => ipv6.innerText = "-")
fetch("/cipher", options={mode: "cors"}).then((r) => r.text()).then((t) => cipher.innerText = t).catch(() => cipher.innerText = "-")
fetch("/useragent", options={mode: "cors"}).then((r) => r.text()).then((t) => useragent.innerText = t).catch(() => useragent.innerText = "-")
//needs to be last in html so alsos last here
fetch("/dns", options={mode: "cors"}).then((r) => r.json()).then((j) => writearray(j,dns)).catch(() => dns.innerText = "-")