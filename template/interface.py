import sys

from template.package_summary import packages_summary
from template.status_check import check_status
from template.truck_report import truck_report

menu_selection = 0

'''
time_now = datetime.now()
"It is currenty ___ time, 1: check realtime package status  2: check status at a specific time

input_time = input('Enter a time (HH:MM:SS): ')
                (hrs, mins, secs) = input_time.split(':')
                convert_user_time = datetime.timedelta(hours=int(hrs), minutes=int(mins), seconds=int(secs))

'''


def menu_response(selection, distances, packages):
    if selection == '1':
        check_status(packages)
    elif selection == '2':
        packages_summary(packages)
    elif selection == '3':
        print(truck_report())
    elif selection == '4':
        print('\n\nSee you next time!')
        sys.exit()
    else:
        print(
            '\nPlease enter a number between 1 and 4 to make your selection.\n'
        )
        print_menu()
        menu_selection = input()
        print(menu_selection)


def print_menu():
    print(
        '----------- WGUPS DLD Monitoring Service  -----------\n\n'

        'Select a menu option and press enter:\n'

        '1 - Check Package Status\n'
        '2 - View All Packages\n'
        '3 - Truck Report\n'
        '4 - End Shift\n\n'

    )
    selection = input()
    menu_response(menu_selection, distances, packages)
