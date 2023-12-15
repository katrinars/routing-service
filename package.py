import datetime
import csv


class PackageHash:

    def __init__(self):
        self.size = 40
        self.table = [[] for _ in range(self.size)]

    def get_hash(self, package_id):
        index = hash(package_id) % self.size
        bucket = self.table[index]

        return bucket

    #
    def insert(self, package_id, package_data):

        bucket = self.get_hash(package_id)
        p = [package_id, package_data]

        if bucket in self.table:
            for package in bucket:
                if package[0] == package_id:
                    package[1] = package_data
                    return True

            bucket.append(p)
            return True

    #
    def lookup(self, package_id):
        bucket = self.get_hash(package_id)
        if bucket in self.table:
            for package in bucket:
                if package[0] == package_id:
                    return package[1]
                else:
                    raise LookupError(f"There is no record of Package {package_id}")
        else:
            raise LookupError("Something went wrong with the lookup function. Try again.")


# create Package class to access data later
class Package:
    """

    """

    #
    def __init__(self, package_id, address, city, state, zip_code, deadline, weight, notes):
        self.package_id = package_id
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.deadline = deadline
        self.weight = weight
        self.notes = notes
        self.status = "at hub"
        self.dispatch_time = datetime.datetime.strptime("00:00", '%H:%M')
        self.delivery_time = datetime.datetime.strptime("00:00", '%H:%M')
        self.tag = []

    #
    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s %s, %s, %s" % (
            self.package_id, self.address, self.city, self.state, self.zip_code,
            self.weight, self.deadline, self.notes, self.status, self.delivery_time)


dldPackages = PackageHash()


def read_packages():
    """
    Read package data from csv file and sort packages into load list based on notes, deadlines, and locations.
    :return: sorted Package Hash Table
    :return: list of load lists
    """
    buddies = set()
    loads = {1: [], 2: [], 3: []}
    sort_list = []
    loaded_list = []

    with (open('csv/packages.csv') as package_file):
        package_reader = csv.reader(package_file, delimiter=',')
        next(package_reader)

        # Store data from rows into variables from csv header. Create time object for package deadlines.
        for rows in package_reader:
            package_id = int(rows[0])
            address = rows[1]
            city = rows[2]
            state = rows[3]
            zip_code = rows[4]
            deadline = datetime.datetime.strptime(rows[5], '%H:%M %p').time() if rows[5][0].isnumeric() else datetime.datetime.strptime("11:59 pm", '%H:%M %p').time()
            weight = rows[6]
            notes = rows[7]

            # Create Package object for each row and insert into hash table
            p = Package(package_id, address, city, state, zip_code, deadline, weight, notes)
            dldPackages.insert(package_id, p)

            to_sort = [package_id, address, zip_code, deadline, notes]
            sort_list.append(to_sort)
            sort_copy = sort_list.copy()

        '''
        Iterate through the list of packages to sort to find and place packages with mandatory truck placements.
        '''
        for parsel in enumerate(sort_list):

            package_id, address, zip_code, deadline, notes = parsel[1][0:5]

            # If the notes specify placement on a specific truck, add the package_id to the load list for that truck.
            if 'on truck' in notes:
                the_truck = notes.split()[-1]
                loads[int(the_truck)].append(package_id)
                loaded_list.append(parsel[1])
                continue


            # Else, if the notes indicate that the package's address will be updated later, add the package to the load list for the latest truck departure.
            elif 'Wrong address' in notes:
                loads[3].append(package_id)
                loaded_list.append(parsel[1])
                continue


            # Else, if the package must be delivered with other packages, find the package_id for each package in the group and add to the buddies set.
            elif 'delivered with' in notes:
                pointer = notes.find('with') + 5
                group = notes[pointer:].split(', ')
                buddies.add(package_id)
                for each in group:
                    buddies.add(int(each))


            # Else, if the notes indicate the package will be delayed, find the time the package arrives, then sort based on truck departure time.
            elif 'Delayed' in notes:
                departure = notes.split(' ')
                for string in departure:
                    if string[0].isnumeric():
                        departure = datetime.datetime.strptime(string, '%H:%M').time()
                if departure.hour < 9:
                    loads[1].append(package_id)
                    loaded_list.append(parsel[1])
                    continue

                elif departure.hour < 10 or departure.hour == 10 and departure.minute < 20:
                    loads[2].append(package_id)
                    loaded_list.append(parsel[1])
                    continue

                else:
                    loads[3].append(package_id)
                    loaded_list.append(parsel[1])
                    continue

        # For the package_id's in buddies, add them all to load 1, then remove any that are present from any other loads.
        for parsel in sort_list:
            for buddy in buddies:
                if parsel[0] == buddy:
                    if buddy in loads[1]:
                        continue
                    else:
                        loads[1].append(parsel[0])
                    loaded_list.append(parsel)
                    if buddy in loads[2]:
                        loads[2].remove(buddy)
                    if buddy in loads[3]:
                        loads[3].remove(buddy)
                continue

        # Remove packages that have been assigned to a truck from the sort list
        for p_id in loads[1], loads[2], loads[3]:
            for the_id in p_id:
                for parsel in sort_copy:
                    if int(parsel[0]) == the_id:
                        sort_list.remove(parsel)
                continue

        sort_copy = sort_list

        # Add priority deadline packages to load 1 or 2 if packages in load have a matching address or zip code.
        for load in loads[1], loads[2]:
            for loaded in loaded_list:
                if loaded[0] in load:
                    for parsel in sort_copy:
                        if parsel[1] == loaded[1] and parsel[3] != '23:59' or parsel[2] == loaded[2] and parsel[3] != '23:59':
                            if len(load) < 16:
                                load.append(parsel[0])
                                sort_list.remove(parsel)

        sort_copy = sort_list

        # Add priority deadline packages with no matching address or zip code to first available load.
        for load in loads[1], loads[2]:
            for loaded in loaded_list:
                if loaded[0] in load:
                    for parsel in sort_copy:
                        if parsel[3] != '23:59':
                            if len(load) < 16:
                                load.append(parsel[0])
                                sort_list.remove(parsel)

        sort_copy = sort_list

        # Add 'EOD' deadline packages to any load with a matching address
        for load in loads[1], loads[2], loads[3]:
            for loaded in loaded_list:
                if loaded[0] in load:
                    for parsel in sort_copy:
                        if parsel[1] == loaded[1]:
                            if len(load) < 16:
                                load.append(parsel[0])
                                sort_list.remove(parsel)

        sort_copy = sort_list

        # Add 'EOD' deadline packages to any load with a matching zip code
        for load in loads[1], loads[2], loads[3]:
            for loaded in loaded_list:
                if loaded[0] in load:
                    for parsel in sort_copy:
                        if parsel[2] == loaded[2]:
                            if len(load) < 16:
                                load.append(parsel[0])
                                sort_list.remove(parsel)

        # Add remaining packages to the load with the least number of packages, as long as it stays under capacity.
        for parsel in sort_list.copy():
            if len(loads[1]) < 16 and len(loads[1]) < len(loads[2]) and len(loads[1]) < len(loads[3]):
                load.append(parsel[0])
                sort_list.remove(parsel)
            elif len(loads[1]) < 16 and len(loads[1]) < len(loads[2]) and len(loads[1]) < len(loads[3]):
                load.append(parsel[0])
                sort_list.remove(parsel)
            elif len(loads[3]) < 16 and len(loads[3]) < len(loads[2]) and len(loads[3]) < len(loads[1]):
                load.append(parsel[0])
                sort_list.remove(parsel)
            else:
                raise IndexError('There is no space in the trucks')

        return sorted(dldPackages.table), loads
