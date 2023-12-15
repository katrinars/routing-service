def packages_summary(packages):
    id_header = 'ID'
    address_header = 'DELIVERY ADDRESS'
    kg_header = 'KG'
    deadline_header = 'DEADLINE'
    notes_header = 'NOTES'
    status_header = 'STATUS'
    d_time_header = 'DELIVERY TIME'



print('{:^145}'.format('----------------------------------------------------------------------'))
print('{:^145}'.format('                         DAILY PACKAGES SUMMARY                       '))
print('{:^145}'.format('----------------------------------------------------------------------'))
print('\n')
print('%-10s %-33s %-15s %-20s         %-27s %-12s %-15s' % (
    id_header, address_header, kg_header,
    deadline_header, notes_header, status_header, d_time_header))
print()

for p in packages.table:
    summary = packages.lookup(p[0][0])
    p_id = summary[0]
    address = summary[1][:26]
    weight = summary[5]
    deadline = summary[6]
    notes = summary[7]
    status = summary[8]
    d_time = summary[9]

    print('%-10s %-33s %-15s %-20s %-33s %-15s %-15s' % (
        p_id, address, weight, deadline, notes, status, d_time))

    # press 9 to go back to menu