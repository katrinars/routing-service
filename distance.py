import csv


def read_distances():
    with open('./csv/distances.csv') as distance_file:
        distance_reader = csv.reader(distance_file)
        addresses = next(distance_reader)[2:]

        # Initialize a list for the distance cells with a temporary value of None
        distances = [[None] * len(addresses) for _ in range(len(addresses))]

        # For each row, starting in the second column, add the distance at the row/column intersection to the distances list.
        for i, row in enumerate(distance_reader):
            for j, distance in enumerate(row[2:]):
                distances[i][j] = float(distance) if distance else None

    return distances


def read_locations():
    with open('./csv/distances.csv') as distance_file:
        distance_reader = csv.reader(distance_file, delimiter=',')
        addresses = next(distance_reader)[2:]
        places = []

        for address in addresses:
            the_address = address.splitlines()[1].strip(', ')
            places.append(the_address)

    return places


# send loaded (shuffled + optimized) truck, distances hash, and packages hash
def get_distance(route, distances):
    distance = 0.0
    for i in range(len(route) - 1):
        location1 = route[i]
        location2 = route[i + 1]

        if distances[location1][location2]:
            distance += distances[location1][location2]

        else:
            distance += distances[location2][location1]

    return distance
