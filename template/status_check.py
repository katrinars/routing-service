
def check_status(packages):
    print('TIME:  ')
    search_time = input()
    print('PACKAGE ID:  ')
    p = int(input())

    summary = packages.lookup(p)
    p_id = summary[0]
    address = summary[1][:26]
    weight = summary[5]
    deadline = summary[6]
    notes = summary[7]
    status = summary[8]
    d_time = summary[9]

    print('{:^70}'.format('----------------------------------------------------------------------'))
    print('{:^70}'.format('                         STATUS CHECKUP                       '))
    print('{:^70}'.format('----------------------------------------------------------------------'))
    print('\n')
    print(f'Checking The Status of Package {p_id} at {search_time}....')
    time.sleep(1.5)
    print('\n')
    print(f'Loading...')
    time.sleep(1)
    print(f'--- STATS FOR PACKAGE {p_id} at {search_time} ---'
          f'Delivery Status: {status}'
          f'Location: {address}'
          )
    # if status == 'at hub' or 'in route'
    # print('Estimated Delivery Time: ')
    # else
    # print('Package was delivered at ___)

    print()
    print('%-10s %-33s %-15s %-20s %-33s %-15s %-15s' % (
        p_id, address, weight, deadline, notes, status, d_time))
    print('\n')

    # press 9 to go back to menu




