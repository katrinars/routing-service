import csv


def read_distances():
    """
    Read distances from csv and store the distance values in a 2-dimensional list. - O(n²)

    :return: distances
    """

    with open('./csv/distances.csv') as distance_file:
        distance_reader = csv.reader(distance_file)
        addresses = next(distance_reader)[2:]
        distances = [[None] * len(addresses) for _ in range(len(addresses))]

        # For each row, add the distance at the row/column intersection to the distances list.
        # Default to None if not present.
        for i, row in enumerate(distance_reader):
            for j, distance in enumerate(row[2:]):
                distances[i][j] = float(distance) if distance else None

    return distances


def read_locations():
    """
    Read locations from csv, format addresses to include only the first line, and store in a list. - O(n)

    :return: addresses as "places"
    """

    with open('./csv/distances.csv') as distance_file:
        distance_reader = csv.reader(distance_file, delimiter=',')
        addresses = next(distance_reader)[2:]
        places = []
        for address in addresses:
            form_address = address.splitlines()[1].strip(', ')
            places.append(form_address)

    return places


def get_distance(route, distances):
    """
    Calculates the distance between all the locations in a given route. - O(n)

    :param route: route to calculate distance from
    :param distances: imported distances values
    :return: distance between all locations on the route
    """

    distance = 0.0

    # Create two location variables to compare neighboring locations for the length of the route.
    for i in range(len(route) - 1):
        location1 = route[i]
        location2 = route[i + 1]

        # Increment the distances variable by each new distance found between neighboring locations on the route.
        if distances[location1][location2]:
            distance += distances[location1][location2]
        else:
            distance += distances[location2][location1]


    return distance
