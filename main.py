# created by K. Stradford | Student #011334472

import dispatch

dispatch.dispatch()



'''

 if get_user_need.lower() not in ['1', '2', '3', 'exit']:
            print("IMPROPER INPUT. PLEASE TRY AGAIN.")
            user_interface()

        if get_user_need.lower() == 'exit':
            print("Goodbye.")
            return

# Calculate total distance of the second truck and distance of each package -> O(n)
for index in range(len(distance.second_truck_index())):
    try:
        total_distance_2 = distance.get_distance(int(distance.second_truck_index()[index]), int(distance.second_truck_index()[index + 1]), total_distance_2)

        deliver_package = distance.get_time(distance.get_current_distance(int(distance.second_truck_index()[index]), int(distance.second_truck_index()[index + 1])), second_leave_times)
        distance.second_truck_list()[index][10] = (str(deliver_package))
        csv_reader.get_hash_map().update(int(distance.second_truck_list()[index][0]), second_delivery)
    except IndexError:
        pass'''

'''

while (user_input != "q"):
    print("")

    print(COLORS.OKCYAN + "\tWhat would you like to do?" + COLORS.TERMINATE)
    print("")
    print("\td - Begin Delivery Simulation and Package Information Lookup")
    print("\tq - Quit")
    print("")
    # You have to clear this, otherwise it will fill up with duplicate historical
    # delivery records rofl
    package_status_over_time.clear()
    user_input = input(">").lower()



# Set that will hold packages that have been delievered up to the given time
                        filtered_packages = dict()

                        for package_id in sorted(package_status_over_time["DELIVERED_TIMES"]):
                            if (time.strptime(package_status_over_time["DELIVERED_TIMES"][package_id], "%H:%M:%S") <= selected_time):
                                delivered_time = package_status_over_time["DELIVERED_TIMES"][package_id]
                                package_handler.get_package_by_id(str(package_id)).set_status(
                                    'DELIVERED (' + delivered_time + ')')
                                #filtered_packages[int(package_id)] = package_handler.get_package_by_id(str(package_id))

                            elif ((time.strptime(package_status_over_time["DELIVERED_TIMES"][package_id], "%H:%M:%S") > selected_time) and (time.strptime(package_status_over_time["HUB_DEPARTURE"][package_id], "%H:%M:%S") <= selected_time)):
                                package_handler.get_package_by_id(
                                    str(package_id)).set_status('EN ROUTE')
                                #filtered_packages[int(package_id)] = package_handler.get_package_by_id(str(package_id))

                            elif (time.strptime(package_status_over_time["HUB_DEPARTURE"][package_id], "%H:%M:%S") > selected_time):
                                package_handler.get_package_by_id(
                                    str(package_id)).set_status('AT THE HUB')
                                #filtered_packages[int(package_id)] = package_handler.get_package_by_id(str(package_id))

                            if (str(package_id) == target_id):
                                filtered_packages[int(package_id)] = package_handler.get_package_by_id(
                                    str(package_id))

                        print("")
                        print(
                            f'\tPackage with an ID of ({target_id}) as of (' + time.strftime("%H:%M:%S", selected_time) + ')')
                        print("\t---------------------------------")
                        if ("DELIVERED" in str(filtered_packages[int(target_id)])):
                            print(
                                COLORS.GREEN + "\t"+str(filtered_packages[int(target_id)]) + COLORS.TERMINATE)
                        elif ("EN ROUTE" in str(filtered_packages[int(target_id)])):
                            print(
                                COLORS.YELLOW + "\t"+str(filtered_packages[int(target_id)]) + COLORS.TERMINATE)
                        elif ("AT THE HUB" in str(filtered_packages[int(target_id)])):
                            print(
                                COLORS.RED + "\t"+str(filtered_packages[int(target_id)]) + COLORS.TERMINATE)
                                '''
