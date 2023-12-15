import truck


def truck_report():
    print('{:^145}'.format('----------------------------------------------------------------------'))
    print('{:^145}'.format('                            DAILY TRUCK RECAP                          '))
    print('{:^145}'.format('----------------------------------------------------------------------'))
    print(
        f'\nTOTAL MILES TRAVELED: {truck.truck1.miles_traveled} + {truck.truck2.miles_traveled} + {truck.truck3.miles_traveled}')

    print('---------------  TRUCK 1  ----------------')
    print('LOGISTICS')
    print(f'Departure Time: {truck.truck1.departure_time}')
    print(f'Driver: {truck.truck1.driver}')
    print(f'Package List: {truck.truck1.packages}')
    print(f'Final Location: {truck.truck1.location}')

    print('PERFORMANCE')
    print(f'Route Completion Time: 00:00')
    print(f'Miles Traveled: {truck.truck1.miles_traveled}')
    print('\n\n')

    print('---------------  TRUCK 2  ----------------')
    print('LOGISTICS')
    print(f'Departure Time: {truck.truck2.departure_time}')
    print(f'Driver: {truck.truck2.driver}')
    print(f'Package List: {truck.truck2.packages}')
    print(f'Final Location: {truck.truck2.location}')

    print('PERFORMANCE')
    print(f'Route Completion Time: 00:00')
    print(f'Miles Traveled: {truck.truck2.miles_traveled}')
    print('\n\n')

    print('---------------  TRUCK 3  ----------------')
    print('LOGISTICS')
    print(f'Departure Time: {truck.truck3.departure_time}')
    print(f'Driver: {truck.truck3.driver}')
    print(f'Package List: {truck.truck3.packages}')
    print(f'Final Location: {truck.truck3.location}')

    print('PERFORMANCE')
    print(f'Route Completion Time: 00:00')
    print(f'Miles Traveled: {truck.truck3.miles_traveled}')
    print('\n\n')

    # press 9 to go back to menu