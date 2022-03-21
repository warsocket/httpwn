var cachelist = [
	'./',
	'./index.html',
	'./index.css',
	'./index.js',
	'./manifest.json',
	'./icon-1024.png',
	'./icon-192.png',
	'./Shape-Cube-512.png'
]


self.addEventListener('install', (event) => {

	event.waitUntil(
		caches.delete('httpwncache').then(() => {
			caches.open('httpwncache').then((cache) => {
				return cache.addAll(cachelist);
			})
		})
	)
});

self.addEventListener('fetch', function (event) {

	var base = this.serviceWorker.scriptURL.slice(0,-this.serviceWorker.scriptURL.split("/").pop().length)
	var targets = cachelist.map( (i) => base + i.slice(i.split("/",1)[0].length+1) )

	if (targets.includes(event.request.url)){
		event.respondWith(
			caches.open('httpwncache').then( () => {
				return caches.match(event.request)
			}).then((response) => {
				return response || fetch(event.request)
			})
		)
	}

});