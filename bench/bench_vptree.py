cities = import all_the_cities
VPTreeFactory = import vptree

rad = Math.PI / 180

n = cities.length
k = 1000

randomPoints = []
for i in range(0, k, 1)
    randomPoints.push(
    lon: -180 + 360 * Math.random(),
    lat: -60 + 140 * Math.random()
    )
  
index = VPTreeFactory.build(cities, distance)

index.search({lon: -119.7051, lat: 34.4363}, 1000)

index.search({lon: -119.7051, lat: 34.4363}, 50000)

index.search({lon: -119.7051, lat: 34.4363}, Infinity)

for i in range(0, k, 1):
    index.search({lon: randomPoints[i].lon, lat: randomPoints[i].lat}, 1)

def distance(a, b):
    d = Math.sin(a.lat * rad) * Math.sin(b.lat * rad) + Math.cos(a.lat * rad) * Math.cos(b.lat * rad) * Math.cos((a.lon - b.lon) * rad);
    return 6371 * Math.acos(Math.min(d, 1))
