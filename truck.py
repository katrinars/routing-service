import datetime
from queue import Queue

import distance
import package


class Truck:
    """
    Create the Truck class and assign Truck object attributes.
    """

    def __init__(self, truck_id, departure_time, driver):
        self.id = truck_id
        self.departure_time = datetime.datetime.strptime(departure_time, '%H:%M:%S')
        self.mph = 18
        self.capacity = 16
        self.packages = []
        self.location = 0
        self.miles_traveled = 0
        self.driver = driver
        self.route = []
        # PACKAGE STATUS
        # when truck loaded, "at hub"
        # when truck departs, "en route"
        # when truck hits location, "delivered"



'''
TODO: create function to remove packages that were loaded from the list, call after loops are done
'''

# initialize 3 trucks - O(1)
trucks = [Truck(1, '08:00:00', 1),
          Truck(2, '09:06:00', 2),
          Truck(3, '10:21:00', None)]


def load_trucks():
    """
    Load the 3 trucks by prioritizing notes, deadlines, and zip codes.
    Create a package tracking list to ensure all packages are accounted for.

    :return: A list containing the final list of assigned packages for each truck - or an error.
    """

    packages, loads = package.read_packages()

    # Load initial packages onto trucks based on dispatch_constraints. - O(n)
    for truck in trucks:
        for parsel in loads[truck.id]:
            truck.packages.append(packages[int(parsel) - 1])

    # Remove assigned packages from the package tracking list. - O(n²)
    for truck in trucks:
        for parsel in loads[truck.id].copy():
            for data in truck.packages:
                if data[0] == parsel:
                    loads[truck.id].remove(parsel)

    # Create a list containing lists of each truck's package load. - O(1)
    final_loads = [[trucks[0].packages], [trucks[1].packages], [trucks[2].packages]]

    # If all packages are loaded, return final truck loads. If not, raise an error. - O(1)
    if sum(len(truck.packages) for truck in trucks) == 40:
        return final_loads
    else:
        raise ValueError(f'Packages {[p for p in loads]} were not loaded.')


def get_delivery_times(distances, places):
    for the_truck in trucks:
        print(the_truck.route)

        for parsel in package.dldPackages.table:
            if parsel in the_truck.packages:
                parsel[0][1].dispatch_time = the_truck.departure_time
                for location in the_truck.route:
                    miles = distance.get_distance((the_truck.location, location), distances)
                    the_truck.miles_traveled += miles
                    the_truck.location = location
                    time_to_location = (the_truck.miles_traveled / the_truck.mph)
                    time_to_deliver = datetime.timedelta(hours=time_to_location)
                    if parsel[0][1].address == places[location]:
                        parsel[0][1].delivery_time = parsel[0][1].dispatch_time + time_to_deliver
                        print(
                            f'PARSEL {parsel[0][1].package_id} leaves at {parsel[0][1].dispatch_time} and arrives at {parsel[0][1].delivery_time}')
    return True


