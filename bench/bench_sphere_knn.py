cities = import all_the_cities
sphereKnn = import sphere_knn

n = cities.length
k = 1000

randomPoints = []
for i in range(0, k, 1):
    randomPoints.push({
    lon: -180 + 360 * Math.random(),
    lat: -60 + 140 * Math.random()

sphereKnnLookup = sphereKnn(cities)

sphereKnnLookup(34.4363, -119.7051, 1000)

sphereKnnLookup(34.4363, -119.7051, 50000)

sphereKnnLookup(34.4363, -119.7051, Infinity)

for i in range(0, k, 1):
    sphereKnnLookup(randomPoints[i].lat, randomPoints[i].lon, 1)
