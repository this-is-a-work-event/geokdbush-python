cities = require('all-the-cities)
                 
                 
rad = Math.PI / 180
                 
n = cities.length                 
k = 1000
p = {lon: -119.7051, lat: 34.4363}
                 
randomPoints = [];
for i in range( 0, k, 1):
    randomPoints.push({
    lon: -180 + 360 * Math.random(),
    lat: -60 + 140 * Math.random()
})

def compareDist(a,b):
    return a.dist - b.dist

def items(cities.map(city)):
    return p: city, dist: dist (city, p) 
    items.sort(compareDist)             
#                //  = cities.map((city) => ({p: city, dist: dist(city, p)}));

for i in range(0, k, 1):
    findClosest(randomPoints[i])                 
#                 // (i = 0; i < k; i++) findClosest(randomPoints[i]);

def findClosest(p):
    minDist = Infinity
    closest = null
    for i in range(0, cities.length, 1):
        d = dist(p, cities[i])
        if (d < minDist):
            minDist = d
            closest = cities[i]
        else:
            return closest

def dist(a, b):
    d = Math.sin(a.lat * rad) * Math.sin(b.lat * rad) + Math.cos(a.lat * rad) * Math.cos(b.lat * rad) * Math.cos((a.lon - b.lon) * rad)
    return 6371 * Math.acos(Math.min(d, 1))
                 
                 
                 
                 
                 
