import datetime
import random
from math import inf
import distance
import package
import truck


def dispatch():
    """
    Find the best route for each truck based on the packages it has.

    :return: the distance each truck will travel based on the best route that is found
    """

    packages = package.read_packages()
    distances = distance.read_distances()
    places = list(distance.read_locations())

    # Load the trucks with packages based on criteria
    truck.load_trucks()

    # Initialize the final distance to a maximum number for replacement.
    # Group distance, route, and truck variables into lists.
    final_distances = [inf, inf, inf]
    final_routes = [[], [], []]

    # Pass each truck through the 2 Opt algorithm 100 times to find the best route.
    # Update the final routes and distances after each better route is found.
    for _ in range(100):
        for i, the_truck in enumerate(truck.trucks):
            final_routes[i] = three_opt(the_truck, distances, places)
            final_distances[i] = update_route(the_truck, final_routes[i], final_distances[i], distances, places)

    print(f'final distance truck 1: {final_distances[0]}')
    print(f'final distance truck 2: {final_distances[1]}')
    print(f'final distance truck 3: {final_distances[2]}')
    print(f"TOTAL FINAL DISTANCE: {sum(final_distances)}")
    print()

    # Pass routed truck to a function where delivery simulation will begin.
    truck.get_delivery_times(distances, places)


def three_opt(the_truck, distances, places):
    start_location = places.index('4001 South 700 East')
    random.shuffle(the_truck.packages)
    locations = []

    for parsel in the_truck.packages:
        p_id = parsel[0][0]
        location = package.dldPackages.lookup(p_id)
        for place in places:
            if place == location.address:
                locations.append(places.index(place))
                continue

    locations = list(set(locations))
    random.shuffle(locations)
    best_route = locations
    improved = True
    while improved:
        improved = False
        for i in range(1, len(the_truck.packages) - 3):
            for j in range(i + 1, len(the_truck.packages) - 2):
                for k in range(j + 1, len(the_truck.packages) - 1):
                    new_route = locations[:i] + locations[i:j + 1][::-1] + locations[j + 1:k + 1][::-1] + locations[
                                                                                                          k + 1:]
                    start_of_best_route = [start_location, best_route[0]]
                    start_of_new_route = [start_location, new_route[0]]
                    best_starting_distance = distance.get_distance(start_of_best_route, distances)
                    new_starting_distance = distance.get_distance(start_of_new_route, distances)
                    if (distance.get_distance(new_route, distances) + new_starting_distance) < (
                            distance.get_distance(best_route, distances) + best_starting_distance):
                        best_route = new_route
                        improved = True

    return best_route


def update_route(the_truck, final_route, final_distance, distances, places):
    """

    :param places:
    :param the_truck:
    :param final_route:
    :param final_distance:
    :param distances:
    :return:
    """
    start_location = places.index('4001 South 700 East')
    new_distance = distance.get_distance(final_route, distances)
    if new_distance < final_distance:
        final_distance = new_distance
        final_route.insert(0, start_location)
        the_truck.route = final_route

    return final_distance

