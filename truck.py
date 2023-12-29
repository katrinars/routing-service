import datetime
import distance
import package


class Truck:
    """
    Class to represent a truck object.
    """

    def __init__(self, truck_id, departure_time, driver):
        """
        Initialize the truck object. - O(1)

        :param truck_id: integer ID value of the truck
        :param departure_time: datetime object representing the time the truck leaves the WGU Hub
        :param driver: integer value 1 or 2 reprsenting the truck driver
        """
        self.id = truck_id
        self.departure_time = datetime.datetime.strptime(departure_time, '%H:%M:%S')
        self.mph = 18
        self.capacity = 16
        self.packages = []
        self.location = 0
        self.miles_traveled = 0
        self.driver = driver
        self.route = []


# Create three truck objects.
trucks = [Truck(1, '08:00:00', 1),
          Truck(2, '09:06:00', 2),
          Truck(3, '10:21:00', 1)]


def load_trucks(loads):
    """
    Loads trucks from the packages hash table based on the sorted loads. - O(n²)

    :param loads: list of truck loads filled with package IDs
    :return: list of Truck objects
    """
    # Add package IDs to the corresponding truck's package list. - O(n)
    for load in loads[1]:
        trucks[0].packages.append(package.dldPackages.lookup(load))
    for load in loads[2]:
        trucks[1].packages.append(package.dldPackages.lookup(load))
    for load in loads[3]:
        trucks[2].packages.append(package.dldPackages.lookup(load))

    # Specify each truck as an attribute for its associated packages. - O(n²)
    for truck in trucks:
        for parcel in truck.packages:
            parcel.truck = truck.id

    return trucks


def take_route(query_time, the_truck, distances):
    """
    Calculate the progress of a truck at the query time. - O(n)

    :param query_time: the user input time or the time the user started the program
    :param the_truck: the specified truck to calculate the progress for
    :param distances: the imported distances between each location
    :return: the miles traveled and the final location for the truck once the query time is reached
    """
    current_time = the_truck.departure_time
    progress_location = 0
    progress_miles = 0

    # Loop the truck route and update the latest truck location until the query time is reached.
    for i in range(len(the_truck.route) - 1):
        if current_time.time() < query_time:
            progress_location = the_truck.route[i]
            next_location = the_truck.route[i + 1]

            # Increment miles and delivery time as each new location is reached.
            travel_distance = distance.get_distance((progress_location, next_location), distances)
            progress_location = next_location
            progress_miles += travel_distance
            time_to_location = travel_distance / the_truck.mph
            current_time += datetime.timedelta(hours=time_to_location)
        else:
            return progress_location, progress_miles

    return progress_location, progress_miles
