import datetime
import csv


class PackageHash:
    """
    Class that constructs a hash table to store the package objects.

    (Western Governors University, 2022)
    """
    load_factor = 1.5
    num_packages = 0

    def __init__(self):
        """
        Initialize the hash table with 40 empty bucket lists. - O(1)
        """
        self.size = 40
        self.table = [[] for _ in range(self.size)]


    def get_hash(self, package_id):
        """
        Get the hash of a package using the package ID key. - O(1)
        """
        index = hash(package_id) % self.size
        bucket = self.table[index]

        return bucket

    def insert(self, package_id, package_data):
        """
        Insert or update a package using the package ID key and the package data list as the value. - O(n)
        """
        bucket = self.get_hash(package_id)
        p = [package_id, package_data]

        if bucket in self.table:
            for package in bucket:
                if package[0] == package_id:
                    package[1] = package_data
                    return True

            bucket.append(p)
            return True

        # track number of entries for rehashing at 150% capacity
        self.num_packages += 1
        load = self.num_packages / self.size
        if load > self.load_factor:
            self.resize()

    def lookup(self, package_id):
        """
        Look up a package using the package ID. - O(n)
        """
        bucket = self.get_hash(package_id)
        if bucket in self.table:
            for package in bucket:
                if package[0] == package_id:
                    return package[1]
                else:
                    raise LookupError(f"There is no record of Package {package_id}")
        else:
            raise LookupError("Something went wrong with the lookup function. Try again.")

    def resize(self):
        """
        Resize the hash table to fit the package size and copy over the existing values. - O(n²)

        (GeeksforGeeks, 2023)
        """
        # Copy existing packages into a temporary list.
        temp_packages = []
        for package in self.table:
            temp_packages.append(package)

        # Create a new empty hash table and double the size
        self.__init__()
        self.size = self.size * 2
        self.table = [[] for _ in range(self.size)]

        # Insert the packages from the temporary list into the new hash table.
        for package_id, package_data in temp_packages:
            self.insert(package_id, package_data)


class Package:
    """
    Class that constructs and holds package objects.
    """

    def __init__(self, package_id, address, city, state, zip_code, deadline, weight, notes, truck):
        """
        Initialize the package object with the package csv headers as attributes. - O(1)
        """
        self.package_id = package_id
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.deadline = deadline
        self.weight = weight
        self.notes = notes
        self.status = "at the hub"
        self.dispatch_time = datetime.datetime.strptime("00:00", '%H:%M')
        self.delivery_time = datetime.datetime.strptime("00:00", '%H:%M')
        self.truck = None

    def __str__(self):
        """
        Return a string representation of the package object. - O(1)
        """
        return "%s, %s, %s, %s, %s, %s, %s %s, %s, %s" % (
            self.package_id, self.address, self.city, self.state, self.zip_code,
            self.weight, self.deadline, self.notes, self.status, self.delivery_time)


dldPackages = PackageHash()  # Create an instance of the package hash table.


def read_packages():
    """
    Read the packages csv and sort the packages into truck load lists based on notes, deadlines, and locations. - O(n)

    :return: list of loads, which are filled with package IDs for the packages to load onto each truck.
    """


    buddies = set()
    loads = {1: [], 2: [], 3: []}
    sort_list = []
    loaded_list = []
    EOD = datetime.datetime.strptime("16:59:59", '%H:%M:%S')

    with (open('csv/packages.csv') as package_file):
        package_reader = csv.reader(package_file, delimiter=',')
        next(package_reader)

        # Store data from rows into variables corresponding to the Package class attributes.
        for rows in package_reader:
            package_id = int(rows[0])
            address = rows[1]
            city = rows[2]
            state = rows[3]
            zip_code = rows[4]
            deadline = datetime.datetime.strptime(rows[5], '%H:%M %p') if rows[5][0].isnumeric() else EOD
            weight = rows[6]
            notes = rows[7]
            truck = None

            # Create Package object for each row and insert it into the hash table instance.
            p = Package(package_id, address, city, state, zip_code, deadline, weight, notes, truck)
            dldPackages.insert(package_id, p)

            # Insert the packages into a sort list for tracking. Copy the list to avoid removal and iteration errors.
            sort_list.append(p)
        sort_list.sort(key=lambda package: package.deadline)
        sort_copy = sort_list.copy()

        # Sort each package in the sort list into a load list via the sorting criteria.
        for parcel in sort_list:
            if parcel.notes:

                # If the notes specify placement on a specific truck, add the package_id to the corresponding load list.
                if 'on truck' in parcel.notes:
                    the_truck = parcel.notes.split()[-1]
                    loads[int(the_truck)].append(parcel.package_id)
                    loaded_list.append(parcel)
                    continue


                # If the address will be updated later, add the package to the Truck 3 load list.
                elif 'Wrong address' in parcel.notes:
                    loads[3].append(parcel.package_id)
                    loaded_list.append(parcel)
                    continue


                # If the package must be delivered with other packages, add all related package IDs to the list for Truck 1.
                elif 'delivered with' in parcel.notes:
                    pointer = parcel.notes.find('with') + 5
                    group = parcel.notes[pointer:].split(', ')
                    buddies.add(parcel.package_id)
                    loaded_list.append(parcel)
                    if parcel.package_id not in loads[1]:
                        loads[1].append(parcel.package_id)
                        for buddy in group:
                            buddies.add(int(buddy))
                            for p in sort_copy:
                                if int(buddy) == p.package_id and p.package_id not in loads[1]:
                                    loads[1].append(p.package_id)
                                    loaded_list.append(p)


                # If the package will be delayed, find the hub arrival time and sort into lists based on truck departure.
                elif 'Delayed' in parcel.notes:
                    departure = parcel.notes.split(' ')
                    for string in departure:
                        if string[0].isnumeric():
                            departure = datetime.datetime.strptime(string, '%H:%M').time()
                    if departure.hour < 9:
                        loads[1].append(parcel.package_id)
                        loaded_list.append(parcel)
                        continue

                    elif departure.hour < 10 or departure.hour == 10 and departure.minute < 20:
                        loads[2].append(parcel.package_id)
                        loaded_list.append(parcel)
                        continue

                    else:
                        loads[3].append(parcel.package_id)
                        loaded_list.append(parcel)
                        continue

        # Remove packages that have been assigned to a load list from the sort list.
        for p_id in loads[1], loads[2], loads[3]:
            for the_id in p_id:
                for parcel in sort_copy:
                    if parcel.package_id == the_id:
                        sort_list.remove(parcel)
                continue

        sort_copy = sort_list.copy()
        locales1, locales2, locales3 = [], [], []

        # Get list of addresses and zip codes for packages in each load list as locales.
        for load in loads[1]:
            for loaded in loaded_list:
                if loaded.package_id == load:
                    locales1.append(loaded.address)
                    locales1.append(loaded.zip_code)
        for load in loads[2]:
            for loaded in loaded_list:
                if loaded.package_id == load:
                    locales2.append(loaded.address)
                    locales2.append(loaded.zip_code)
        for load in loads[3]:
            for loaded in loaded_list:
                if loaded.package_id == load:
                    locales3.append(loaded.address)
                    locales3.append(loaded.zip_code)

        # Add early deadline packages to load list 1 if the address or zip code matches an already-present locale.
        for parcel in sort_copy:
            if parcel.deadline != EOD:
                if parcel.address in locales1 and len(loads[1]) < 16 or parcel.zip_code in locales1 and len(
                        loads[1]) < 16:
                    loads[1].append(parcel.package_id)
                    loaded_list.append(parcel)
                    sort_list.remove(parcel)

        sort_copy = sort_list.copy()

        # Add early deadline packages with no matching locale to load 1. Exit loop when EOD is reached.
        for parcel in sort_copy:
            if parcel.deadline != EOD:
                loads[1].append(parcel.package_id)
                sort_list.remove(parcel)
            elif parcel.deadline == EOD:
                break

        sort_copy = sort_list.copy()

        # Add remaining packages to any load under capacity with a matching address.
        for load in loads[1], loads[2], loads[3]:
            for loaded in loaded_list:
                if loaded.package_id in load:
                    for parcel in sort_copy:
                        if parcel.address == loaded.address:
                            if len(load) < 16:
                                load.append(parcel.package_id)
                                sort_list.remove(parcel)

        sort_copy = sort_list

        # Add remaining packages to any load under capacity with a matching zip code.
        for load in loads[1], loads[2], loads[3]:
            for loaded in loaded_list:
                if loaded.package_id in load:
                    for parcel in sort_copy:
                        if parcel.zip_code == loaded.zip_code:
                            if len(load) < 16:
                                load.append(parcel.package_id)
                                sort_list.remove(parcel)

        # Add remaining packages to the load with the least number of packages, or raise error if all loads at capacity.
        for parcel in sort_list.copy():
            if len(loads[1]) < 16 and len(loads[1]) < len(loads[2]) and len(loads[1]) < len(loads[3]):
                load.append(parcel.package_id)
                sort_list.remove(parcel)
            elif len(loads[2]) < 16 and len(loads[2]) < len(loads[1]) and len(loads[2]) < len(loads[3]):
                load.append(parcel.package_id)
                sort_list.remove(parcel)
            elif len(loads[3]) < 16 and len(loads[3]) < len(loads[2]) and len(loads[3]) < len(loads[1]):
                load.append(parcel.package_id)
                sort_list.remove(parcel)
            else:
                raise IndexError('There is no space in the trucks')

        return loads


def update_statuses(query_time):
    """
    Update the statuses of each package based on the query time and its dispatch and delivery times. - O(n)

    :param query_time: the user input time or the current time at the start of the program
    """
    for i in range(1, 41):
        p = dldPackages.lookup(i)

        if query_time < p.dispatch_time.time():
            p.status = "at the hub"
        elif p.dispatch_time.time() <= query_time < p.delivery_time.time():
            p.status = "en route"
        elif query_time >= p.delivery_time.time():
            p.status = "delivered"
