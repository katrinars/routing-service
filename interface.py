import datetime
import sys
import distance
import package
import truck


def interface_main():
    """
    Print menu with the option to generate reports based on the current time or a custom input time.
    """

    # Loop a menu with time options until a valid entry is made, then route to the correct menu.
    while True:
        print(
            '\033[1;36;40m----------- WGU Postal Service -----------\n'
            '  Daily Local Delivery Monitoring Service   \n\n\n'

            '\033[1;36;40mCHOOSE A TIME OPTION:\n\n'
            '\033[0;37;40m1: Get Realtime Updates\n'
            '2: Get Updates at a Specific Time\n\n'
        )

        time_input = input('\033[0;36;40mEnter a menu option number and press enter: ')
        if time_input == '1':
            realtime_menu()
            break
        elif time_input == '2':
            user_time_menu()
            break
        else:
            print('\n\n\033[0;31;40mERROR: Please enter a valid menu option and press enter.\n\n')


def realtime_menu():
    """
    Print menu with the option to generate a report on all packages, one specified package, all trucks, or the option
    to exit the program.
    """

    # Get current time, format time, and print report options.
    time_now = datetime.datetime.now().time()

    # Loop through menu with report options until a valid entry is made, then route to the corresponding function.
    while True:
        print(
            f'\033[1;36;40m\n\n\nThe current time is {time_now.strftime('%I:%M %p')}.\n\n'
            '\033[0;37;40m'
            '1 - View All Packages\n'
            '2 - Look Up a Package\n'
            '3 - See Truck Summary\n'
            '4 - Exit the Program\n\n'
        )

        menu_input = input('\033[0;36;40mEnter Your Selection: ')
        if menu_input == '1':
            print(print_all_packages(time_now))
        elif menu_input == '2':
            package_lookup(time_now)
        elif menu_input == '3':
            truck_stats(time_now)
        elif menu_input == '4':
            print('\n\nSee you next time!\n')
            sys.exit()
        else:
            print('\n\n\033[0;31;40mInvalid entry. Please select a number 1-4, then press enter.\n\n')


def user_time_menu():
    """
    Print prompt for the user's time input. Validate the time, then print a menu with the option to generate a report
    showing all packages, one package search, all trucks, or to exit the program.
    """

    # Get user's desired query time and validate or print error and loop until valid, then print report options menu.
    while True:

        query_time = (input('\n\n\n\n\033[1;35;40mEnter the Query Time (HH:MM am/pm): '))
        try:
            query_time = datetime.datetime.strptime(query_time, '%I:%M %p').time()
        except ValueError:
            print('\n\n\033[0;31;40mInvalid entry. Please use 12-hour format, followed by a space and either \'am\' or \'pm\'.\n\n')

        print(f'\033[0;35;40mYou entered {query_time.strftime('%I:%M %p')}.\n\n'

              '\033[1;36;40mREPORT OPTIONS:\n'

              '\033[0;36;40m'
              '1 - View All Packages\n'
              '2 - Look Up a Package\n'
              '3 - See Truck Summary\n'
              '4 - Exit the Program\n\n'
              )

        menu_input = input('\033[0;36;40mEnter Your Selection: ')
        if menu_input == '1':
            print(print_all_packages(query_time))
        elif menu_input == '2':
            package_lookup(query_time)
        elif menu_input == '3':
            truck_stats(query_time)
        elif menu_input == '4':
            print('\n\nSee you next time!\n')
            sys.exit()
        else:
            print('\n\n\033[0;31;40mInvalid entry. Please select a number 1-4, then press enter.\n\n')


def print_all_packages(query_time):
    """
    Print a summary of all packages at the given time.
    :param query_time: the time the user input or the time the user started the program
    """

    # Update status of packages based on query time and populate miles for the day.
    package.update_statuses(query_time)
    total_miles = truck.trucks[0].miles_traveled + truck.trucks[1].miles_traveled + truck.trucks[2].miles_traveled

    # Assign header strings for printing.
    id_header = 'ID'
    address_header = 'DELIVERY ADDRESS'
    deadline_header = 'DEADLINE'
    notes_header = 'NOTES'
    status_header = 'STATUS'
    truck_header = 'TRUCK'
    delivery_header = 'DELIVERY DETAILS'

    # Print report header.
    print('\n\n')
    print('\033[1;36;40m{:^155}'.format('-----------------------------------------------------------------------------------'))
    print('\033[1;36;40m{:^151}'.format('                                 DAILY PACKAGES SUMMARY                             '))
    print('\033[0;36;40m{:^151}'.format(f'                     query time: {query_time.strftime('%I:%M %p')}                 '))
    print('\033[1;36;40m{:^155}'.format('-----------------------------------------------------------------------------------'))
    print('\n')
    print('\033[0;37;40m{:^155}'.format('      NOTE: Projected future delivery times are indicated with ~ for undelivered packages.    '))
    print('\n')
    print('\033[1;36;40m  %-15s %-35s %-22s %-36s %-15s %-12s %-15s\n' % (id_header, address_header, deadline_header,
                                                                          notes_header, status_header, truck_header,
                                                                          delivery_header))

    # Parse package hash table using lookup function to populate package data.
    for i in range(1, 41):
        p = package.dldPackages.lookup(i)
        p_id = p.package_id
        address = p.address[:26]
        deadline = p.deadline.time().strftime('%I:%M %p')
        notes = p.notes
        status = p.status
        the_truck = p.truck
        delivery_time = p.delivery_time.time()
        delivery_details = ''
        if query_time < delivery_time:
            delivery_details = f'~ {delivery_time.strftime('%I:%M %p')}'
        elif query_time >= delivery_time:
            delivery_details = f'{delivery_time.strftime('%I:%M %p')}'

        print('\033[0;36;40m  %-15s %-35s %-22s %-36s %-15s %-12s %15s' % (p_id, address, deadline, notes.split('-')[0],
                                                                           status, the_truck, delivery_details))

    print('\n')

    # Offer user the option to return to menu or exit the program.
    next_input = input('\n\033[1;37;40mEnter 0 to return to the main menu.\nEnter any other key to exit.\n')
    if next_input == '0':
        interface_main()
    else:
        print('\n\n\n\n\033[1;37;40mSee you next time.\n\n\n')
        sys.exit()


def package_lookup(query_time):
    """
    Print a prompt for the package ID of the package the user wants to query, then print a summary of the package's
    details at the given time.
    :param query_time: the time the user input or the time the user started the program
    """

    # Update package statuses.
    package.update_statuses(query_time)

    # Get user's desired package to look up and verify that it is present or print error message and reroute.
    p_query = int(input('\033[1;36;40mEnter a valid Package ID#: '))
    if p_query not in range(1, len(package.dldPackages.table) + 1):
        print('\033[0;31;40mInvalid entry.\nPlease enter a valid package ID.')
        package_lookup(query_time)
    else:
        pass

    parcel = package.dldPackages.lookup(p_query)

    # Print report header.
    print('\n\n\033[1;36;40m{:^145}'.format('----------------------------------------------------------------------'))
    print('{:^145}'.format('                             PACKAGE QUERY                           '))
    print('{:^145}'.format('----------------------------------------------------------------------'))

    # Print package information.
    print('\n\033[0;36;40m')
    print(f'Package ID: {parcel.package_id}\n'
          f'Address: {parcel.address}\n'
          f'City: {parcel.city}\n'
          f'Zip Code: {parcel.zip_code}\n'
          f'Weight(kg): {parcel.weight}\n'
          f'Delivery Deadline: {parcel.deadline.time().strftime('%I:%M %p')}\n'
          f'Notes: {parcel.notes}\n'
          f'Status: {parcel.status}\n'
          f'Truck: {parcel.truck}\n'
          )
    if query_time < parcel.delivery_time.time():
        print(f'\033[1;36;40mProjected Delivery Time: {parcel.delivery_time.time().strftime('%I:%M %p')}')
    elif query_time >= parcel.delivery_time.time():
        print(f'\033[1;36;40mThis package was delivered at {parcel.delivery_time.time().strftime('%I:%M %p')}')

    print()

    # Offer user the option to return to menu or exit the program.
    next_input = input('\n\033[1;37;40mEnter 0 to return to the main menu.\nEnter any other key to exit.\n')
    if next_input == '0':
        interface_main()
    else:
        print('\n\n\n\n\033[1;37;40mSee you next time.\n\n\n')
        sys.exit()


def truck_stats(query_time):
    """
    Print an update of each truck's progress at the specified time.
    :param query_time: the time that the user input or the time the user started the program
    """

    distances = distance.read_distances()
    places = distance.read_locations()

    # Initialize variables.
    truck1_packages = []
    truck2_packages = []
    truck3_packages = []
    progress_miles1 = 0
    progress_miles2 = 0
    progress_miles3 = 0

    # Add truck package ids to list as strings and sort.
    for the_truck in truck.trucks:
        for parcel in the_truck.packages:
            if the_truck.id == 1:
                truck1_packages.append(str(parcel.package_id))
            elif the_truck.id == 2:
                truck2_packages.append(str(parcel.package_id))
            elif the_truck.id == 3:
                truck3_packages.append(str(parcel.package_id))
    truck1_packages.sort()
    truck2_packages.sort()
    truck3_packages.sort()

    locations = distance.read_locations()

    # Print report header.
    print('\n\n\033[1;36;40m{:^145}'.format('----------------------------------------------------------------------'))
    print('{:^145}'.format('                          DAILY TRUCKS SUMMARY                        '))
    print('\033[0;37;40m{:^145}'.format(f'  {query_time.strftime('%I:%M %p')} SNAPSHOT  '))
    print('\033[1;36;40m{:^145}'.format('----------------------------------------------------------------------'))

    # Print Truck 1 data, location, and miles traveled by the query time.
    print('\n\n')
    print('\033[1;36;40m---------------  TRUCK 1  ----------------')
    print('\033[0;34;40mDAILY INFORMATION')
    print(f'\033[0;37;40mDeparture Time: {truck.trucks[0].departure_time.time().strftime('%I:%M %p')}')
    print(f'Driver: {truck.trucks[0].driver}')
    print(f'Today\'s Packages: ' + ', '.join(truck1_packages))
    progress_location1, progress_miles1 = truck.get_truck_progress(query_time, truck.trucks[0], distances)
    print('\n\033[0;34;40mCURRENT PROGRESS')
    print(f'\033[0;37;40mMost Recent Location: {locations[progress_location1]}')
    print(f'Miles Traveled so Far: {round(progress_miles1, 1)}')
    if progress_location1 == truck.trucks[0].route[-1]:
        print('\033[0;35;40mROUTE COMPLETED')
    print('\n')

    # Print Truck 2 data, location, and miles traveled by the query time.
    print('\033[1;36;40m---------------  TRUCK 2  ----------------')
    print('\033[0;34;40mDAILY INFORMATION')
    print(f'\033[0;37;40mDeparture Time: {truck.trucks[1].departure_time.time().strftime('%I:%M %p')}')
    print(f'Driver: {truck.trucks[1].driver}')
    print(f'Today\'s Packages: ' + ', '.join(truck2_packages))
    progress_location2, progress_miles2 = truck.get_truck_progress(query_time, truck.trucks[1], distances)
    print('\n\033[0;34;40mCURRENT PROGRESS')
    print(f'\033[0;37;40mMost Recent Location: {locations[progress_location2]}')
    print(f'Miles Traveled so Far: {round(progress_miles2, 1)}')
    if progress_location2 == truck.trucks[1].route[-1]:
        print('\033[0;35;40mROUTE COMPLETED')
    print('\n')

    print('\033[1;36;40m---------------  TRUCK 3  ----------------')
    print('\033[0;34;40mDAILY INFORMATION')
    print(f'\033[0;37;40mDeparture Time: {truck.trucks[2].departure_time.time().strftime('%I:%M %p')}')
    print(f'Driver: {truck.trucks[2].driver}')
    print(f'Today\'s Packages: ' + ', '.join(truck3_packages))
    progress_location3, progress_miles3 = truck.get_truck_progress(query_time, truck.trucks[2], distances)
    print('\n\033[0;34;40mCURRENT PROGRESS')
    print(f'\033[0;37;40mMost Recent Location: {locations[progress_location3]}')
    print(f'Miles Traveled so Far: {round(progress_miles3, 1)}')
    if progress_location3 == truck.trucks[2].route[-1]:
        print('\033[0;35;40mROUTE COMPLETED')
    print('\n')
    total_miles = progress_miles1 + progress_miles2 + progress_miles3

    # Print the total miles traveled by the query time.
    print(f'\033[1;34;40mTOTAL MILES TRAVELED BY {query_time.strftime('%I:%M %p')}: {round(total_miles, 1)}\n\n')

    # Offer user the option to return to menu or exit the program.
    next_input = input('\n\033[1;37;40mEnter 0 to return to the main menu.\nEnter any other key to exit.\n')
    if next_input == '0':
        interface_main()
    else:
        print('\n\n\n\n\033[1;37;40mSee you next time.\n\n\n')
        sys.exit()
