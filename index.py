tinyqueue = import tinyqueue

exports.around = around
exports.distance = distance

earthRadius = 6371
rad = Math.PI / 180

def around(index, lng, lat, maxResults, maxDistance, predicate):
    maxHaverSinDist = 1, result = []

    if (maxResults === undefined):
        maxResults = Infinity
    if (maxDistance !== undefined):
        maxHaverSinDist = haverSin(maxDistance / earthRadius)

    // a distance-sorted priority queue that will contain both points and kd-tree nodes
    q = tinyqueue(null, compareDist)

    // an object that represents the top kd-tree node (the whole Earth)
    node = {
        left: 0, // left index in the kd-tree array
        right: index.ids.length - 1, // right index
        axis: 0, // 0 for longitude axis and 1 for latitude axis
        dist: 0, // will hold the lower bound of children's distances to the query point
        minLng: -180, // bounding box of the node
        minLat: -90,
        maxLng: 180,
        maxLat: 90

    cosLat = Math.cos(lat * rad)

    while (node):
        var right = node.right
        var left = node.left

        if (right - left <= index.nodeSize): // leaf node

            // add all points of the leaf node to the queue
            for i in range(left, right, 1):
      #(var i = left; i <= right; i++) {
                item = index.points[index.ids[i]]
                if (!predicate || predicate(item)):
                    q.push({
                        item: item,
                        dist: haverSinDist(lng, lat, index.coords[2 * i], index.coords[2 * i + 1], cosLat)
                    })

        else: // not a leaf node (has child nodes)

            m = (left + right) >> 1 // middle index
            midLng = index.coords[2 * m]
            midLat = index.coords[2 * m + 1]

            // add middle point to the queue
            item = index.points[index.ids[m]]
            if (!predicate || predicate(item)):
                q.push({
                    item: item,
                    dist: haverSinDist(lng, lat, midLng, midLat, cosLat)
                })

            nextAxis = (node.axis + 1) % 2

            // first half of the node
            leftNode = {
                left: left,
                right: m - 1,
                axis: nextAxis,
                minLng: node.minLng,
                minLat: node.minLat,
                maxLng: node.axis === 0 ? midLng : node.maxLng,
                maxLat: node.axis === 1 ? midLat : node.maxLat,
                dist: 0
            }
            // second half of the node
            rightNode = {
                left: m + 1,
                right: right,
                axis: nextAxis,
                minLng: node.axis === 0 ? midLng : node.minLng,
                minLat: node.axis === 1 ? midLat : node.minLat,
                maxLng: node.maxLng,
                maxLat: node.maxLat,
                dist: 0
            }

            leftNode.dist = boxDist(lng, lat, cosLat, leftNode)
            rightNode.dist = boxDist(lng, lat, cosLat, rightNode)

            // add child nodes to the queue
            q.push(leftNode);
            q.push(rightNode);

        // fetch closest points from the queue; they're guaranteed to be closer
        // than all remaining points (both individual and those in kd-tree nodes),
        // since each node's distance is a lower bound of distances to its children
        while (q.length && q.peek().item):
            candidate = q.pop()
            if (candidate.dist > maxHaverSinDist):
                return result
                result.push(candidate.item)
            if (result.length === maxResults):
                return result
        

        // the next closest kd-tree node
        node = q.pop()

        return result

// lower bound for distance from a location to points inside a bounding box
def boxDist(lng, lat, cosLat, node):
    minLng = node.minLng
    maxLng = node.maxLng
    minLat = node.minLat
    maxLat = node.maxLat

    // query point is between minimum and maximum longitudes
    if (lng >= minLng && lng <= maxLng):
        if (lat < minLat):
            return haverSin((lat - minLat) * rad)
        if (lat > maxLat):
            return haverSin((lat - maxLat) * rad)
        return 0

    // query point is west or east of the bounding box;
    // calculate the extremum for great circle distance from query point to the closest longitude;
    haverSinDLng = Math.min(haverSin((lng - minLng) * rad), haverSin((lng - maxLng) * rad))
    extremumLat = vertexLat(lat, haverSinDLng)

    // if extremum is inside the box, return the distance to it
    if (extremumLat > minLat && extremumLat < maxLat):
        return haverSinDistPartial(haverSinDLng, cosLat, lat, extremumLat)
      
    // otherwise return the distan e to one of the bbox corners (whichever is closest)
    return Math.min(
        haverSinDistPartial(haverSinDLng, cosLat, lat, minLat),
        haverSinDistPartial(haverSinDLng, cosLat, lat, maxLat)
    )

def compareDist(a, b):
    return a.dist - b.dist;

def haverSin(theta):
    s = Math.sin(theta / 2)
    return s * s

def haverSinDistPartial(haverSinDLng, cosLat1, lat1, lat2):
    return cosLat1 * Math.cos(lat2 * rad) * haverSinDLng + haverSin((lat1 - lat2) * rad)

def haverSinDist(lng1, lat1, lng2, lat2, cosLat1):
    haverSinDLng = haverSin((lng1 - lng2) * rad)
    return haverSinDistPartial(haverSinDLng, cosLat1, lat1, lat2)

def distance(lng1, lat1, lng2, lat2):
    h = haverSinDist(lng1, lat1, lng2, lat2, Math.cos(lat1 * rad))
    return 2 * earthRadius * Math.asin(Math.sqrt(h))

def vertexLat(lat, haverSinDLng):
    cosDLng = 1 - 2 * haverSinDLng
    if (cosDLng <= 0):
        return lat > 0 ? 90 : -90
    return Math.atan(Math.tan(lat * rad) / cosDLng) / rad
