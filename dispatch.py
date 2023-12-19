import datetime
import random
from math import inf
import distance
import package
import truck


def dispatch():
    """
    This function oversees the dispatch process by calling the functions to load the trucks, implement the 3-opt
    algorithm, find the final routes and distances, and ensure all packages are on time. - O(n²)
    """
    # Import all data using csv readers.
    loads = package.read_packages()
    distances = distance.read_distances()
    places = list(distance.read_locations())

    # Load trucks with sorted packages.
    truck.load_trucks(loads)

    # Adjust address for the truck with "wrong address" in the notes. - O(n²)
    for the_truck in truck.trucks:
        for parcel in the_truck.packages:
            parcel.dispatch_time = the_truck.departure_time
            if parcel.package_id == 9:
                parcel.address = '410 S State St'
                parcel.city = 'Salt Lake City'
                parcel.state = 'UT'
                parcel.zip_code = '84111'

    final_distances = [inf, inf, inf]
    final_routes = [[], [], []]

    # Pass trucks through the 3 Opt algorithm 100 times to find the best route and shortest overall distances. - O(n²)
    for _ in range(100):
        for i, the_truck in enumerate(truck.trucks):
            final_routes[i] = three_opt(the_truck, distances, places)
            final_distances[i] = update_route(the_truck, final_routes[i], final_distances[i], distances)

    # Verify that all packages will arrive by their deadline or swap packages between trucks until they will. - O(n²)
    for i in range(len(truck.trucks)):
        for j in range(i + 1, len(truck.trucks)):
            truck1 = truck.trucks[i]
            truck2 = truck.trucks[j]

            if not on_time(truck1, distances, places) or not on_time(truck2, distances, places):
                swap = swap_packages(truck1, truck2, distances, places)


def three_opt(the_truck, distances, places):
    """
    Take the original truck route and remove then swap three locations on the route continuously to try to find a
    shorter overall distance while minimizing paths on the route that cross over others. - O(n³)

    :param the_truck: truck objects with the route to perform the algorithm on
    :param distances: imported distances to s=use for route optimization
    :param places: location indices to use to connect with the distances data structure
    """

    start_location = places.index('4001 South 700 East')
    locations = []

    # Map package addresses to location indices. - O(n²)
    for parcel in the_truck.packages:
        location = parcel.address
        for place in places:
            if place == location:
                locations.append(places.index(place))
                continue

    # Remove duplicate locations and randomize the initial route. - O(1)
    locations = list(set(locations))
    random.shuffle(locations)

    # Insert the WGU Hub at the beginning of the route for each truck, and also at the end for Truck 1. - O(1)
    locations.insert(0, start_location)
    if the_truck.id == 1:
        locations.append(start_location)


    best_route = locations
    improved = True
    while improved:
        improved = False

        # Iterate through the route to select three locations as constants, then reverse different segments of locations
        # between the constant locations to try to find a shorter route. - O(n³)
        for i in range(1, len(the_truck.packages) - 3):
            for j in range(i + 1, len(the_truck.packages) - 2):
                for k in range(j + 1, len(the_truck.packages) - 1):
                    new_route = (locations[:i] + locations[i:j + 1][::-1] + locations[j + 1:k + 1][::-1] +
                                 locations[k + 1:])

                    # Calculate the distance from the WGU Hub to the first route location.
                    start_of_best_route = [start_location, best_route[0]]
                    start_of_new_route = [start_location, new_route[0]]

                    # Calculate the distance of the route.
                    best_starting_distance = distance.get_distance(start_of_best_route, distances)
                    new_starting_distance = distance.get_distance(start_of_new_route, distances)

                    # Determine whether the new or old route is better, with the start location incorporated.
                    if (distance.get_distance(new_route, distances) + new_starting_distance) < (
                            distance.get_distance(best_route, distances) + best_starting_distance):
                        best_route = new_route
                        improved = True

    return best_route


def update_route(the_truck, final_route, final_distance, distances):
    """
    Verifies that the 3-opt best route is an improvement and updates the route of the truck object or keeps it the
    same if the original distance is lower. - O(1)

    :param the_truck: the truck object
    :param final_route: the best route
    :param final_distance: the full distance traveled on the best route
    :param distances: the imported distances between every location
    :return: the new distance or the truck's existing distance, whichever is shorter
    """

    # Replaces the truck distance and route with the new values if they are an improvement. - O(1)
    new_distance = distance.get_distance(final_route, distances)
    if new_distance < final_distance:
        final_distance = new_distance
        the_truck.route = final_route

    return final_distance


def on_time(the_truck, distances, places):
    """
    Track time variables for the truck and package objects. Confirm that all packages will be delivered by their
    deadline. - O(n²)

    :param the_truck: the truck object
    :param distances: the imported distances between every location
    :param places: the imported locations for package delivery
    :return: True if all packages are delivered on time and False otherwise
    """

    current_time = the_truck.departure_time
    the_truck.miles_traveled = 0
    the_truck.location = 0

    # Loop the truck route.
    for i in range(len(the_truck.route) - 1):
        current_location = the_truck.route[i]
        next_location = the_truck.route[i + 1]
        the_truck.location = next_location

        # Increment the miles traveled and arrival time at each location.
        travel_distance = distance.get_distance((current_location, next_location), distances)
        the_truck.miles_traveled += travel_distance
        time_to_location = travel_distance / the_truck.mph
        current_time += datetime.timedelta(hours=time_to_location)

        # Set the departure time for Truck 3 to Truck 1's return to the hub, if after the original departure time.
        if the_truck.id == 1 and the_truck.location == 0 and current_time > truck.trucks[2].departure_time:
            truck.trucks[2].departure_time = current_time

        # Update package object delivery times.
        for parcel in the_truck.packages:
            if places.index(parcel.address) == next_location:
                parcel.delivery_time = current_time

    return all(parcel.delivery_time <= parcel.deadline for parcel in the_truck.packages)


def swap_packages(truck1, truck2, distances, places):
    """
    Swap two packages where at least one is not on time. Confirm swap if packages are now on time or reverse if the
    packages are still not on time. - O(n²)

    :param truck1: truck with the first package
    :param truck2: truck with the second package
    :param distances: imported distances between each location
    :param places: imported locations for each delivery
    :return: True if swap is successful, False otherwise
    """

    # Prepare to swap packages if they don't have notes with special parameters. - O(n²)
    for parcel1 in truck1.packages:
        for parcel2 in truck2.packages:
            if not parcel1.notes and not parcel2.notes:
                current_route1 = truck1.route.copy()
                current_route2 = truck2.route.copy()

                # Remove each package from its truck, then swap trucks and update package's truck attribute.
                truck1.packages.remove(parcel1)
                truck2.packages.remove(parcel2)
                truck1.packages.append(parcel2)
                truck2.packages.append(parcel1)
                parcel2.truck = 1
                parcel1.truck = 2

                # Run new truck routes through 3-opt algorithm for the best route.
                truck1.route = three_opt(truck1, distances, places)
                truck2.route = three_opt(truck2, distances, places)

                # Confirm that new routes are on time and exit.
                if on_time(truck1, distances, places) and on_time(truck2, distances, places):
                    return True

                # Revert changes to each package if new routes are not on time.
                truck1.packages.remove(parcel2)
                truck2.packages.remove(parcel1)
                truck1.packages.append(parcel1)
                truck2.packages.append(parcel2)
                parcel1.truck = 1
                parcel2.truck = 2
                truck1.route = current_route1
                truck2.route = current_route2

    return False
