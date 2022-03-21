//Service Worker installation
if ('serviceWorker' in navigator) navigator.serviceWorker.register('./sw.js')

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
			document.body.appendChild(document.createElement("span"))
			let span = document.createElement("span")
			span.innerText = item
			document.body.appendChild(span)
		}else{
			firstnode.innerText = item
		}

		first = false
	}
}

if (location.protocol == "https:"){
	protoswitch.innerText = "Using HTTPS"
	protoswitch.className = "https"
	protoswitch.addEventListener('click', () => document.location.href = "http:" + document.location.href.substring(document.location.protocol.length))
}else{
	protoswitch.innerText = "Using HTTP"
	protoswitch.className = "http"
	protoswitch.addEventListener('click', () => document.location.href = "https:" + document.location.href.substring(document.location.protocol.length))
}



fetch("/ip", options={mode: "cors"}).then((r) => r.text()).then((t) => ip.innerText = t).catch(() => ip.innerText = "-")
fetch("//ipv4.httpwn.org/ip", options={mode: "cors"}).then((r) => r.text()).then((t) => ipv4.innerText = t).catch(() => ipv4.innerText = "-")
fetch("//ipv6.httpwn.org/ip", options={mode: "cors"}).then((r) => r.text()).then((t) => ipv6.innerText = t).catch(() => ipv6.innerText = "-")
fetch("/cipher", options={mode: "cors"}).then((r) => r.text()).then((t) => cipher.innerText = t).catch(() => cipher.innerText = "-")
fetch("/dns", options={mode: "cors"}).then((r) => r.json()).then((j) => writearray(j,dns)).catch(() => dns.innerText = "-")
