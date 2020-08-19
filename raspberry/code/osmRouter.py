from pyroutelib3 import Router
import sys

class OSMRouter:

    def __init__(self, osmFile, profile):
        self.router = Router(profile, osmFile)

        self.waypoint = None
        self.currentWaypoint = 0

    def planRoute(self, startCoordsGPS, endCoordsGPS):
        start = self.router.findNode(startCoordsGPS[0], startCoordsGPS[1])
        end = self.router.findNode(endCoordsGPS[0], endCoordsGPS[1])

        self.waypoints = None
        status, route = self.router.doRoute(start, end)

        if status == 'success':
            self.waypoints = list(map(self.router.nodeLatLon, route))
            self.waypoints.append((0, 0))

        return  self.waypoints, len(self.waypoints)

    def getNextWaypoint(self):
        waypoint = None
        arrived = False

        if self.currentWaypoint < len(self.waypoints):
            waypoint = self.waypoints[self.currentWaypoint]
            self.currentWaypoint += 1

        if self.currentWaypoint == len(self.waypoints):
            arrived = True

        return waypoint, arrived

if __name__ == "__main__":
    r = OSMRouter("/home/jonas/Documents/englmardorf.osm", "car")
    route, routeLength = r.planRoute((49.001241, 12.827968), (49.000785, 12.828333))
    print(route)
    print(routeLength)

    arrived = False
    while not arrived:
        waypoint, arrived = r.getNextWaypoint()
        print(waypoint, arrived)

