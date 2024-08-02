from copy import deepcopy

def findPathRecur(startAp, endAp, routes, currentPath, finalPaths):
    for route in routes:
        if route[1] == currentPath[-1]:
            routes.remove(route)
    for route in routes:
        if route[0] == currentPath[-1]:
            if route[1] == endAp:
                path = deepcopy(currentPath)
                path.append(endAp)
                finalPaths.append(path)
            else:
                currentPath.append(route[1])
                findPathRecur(startAp, endAp, routes, currentPath, finalPaths)
    currentPath.pop()

def findPath(startAp, endAp, routes):
    routes = deepcopy(routes)
    currentPath = [startAp]
    finalPaths = []
    findPathRecur(startAp, endAp, routes, currentPath, finalPaths)
    return sorted(finalPaths, key=len)

for ap in aps:
    print(findPath(ap, 'JFK', routes))
