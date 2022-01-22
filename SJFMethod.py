from SharedMethod import build_status, is_done, calculate_tat_wt


def list_arrival_SJF(arrival_time, cpu_time):
    process_list = list()
    for i in range(len(arrival_time)):
        if arrival_time[i] <= cpu_time and arrival_time[i] != -1:
            process_list.append(i)

    return process_list


# this function find the next process index that should execute in 'SJF algorithm'
def next_process_SJF(arrival_time, io_finished_at, burst_time_1, burst_time_2, cpu_time):
    list_arrival = list_arrival_SJF(arrival_time, cpu_time)
    list_io_finished = list_arrival_SJF(io_finished_at, cpu_time)
    arrival_flag = False
    min_index_arrival = 0
    min = float('+inf')
    if len(list_arrival) > 1:
        for i in list_arrival:  # find minimum burst time in list_arrival
            if burst_time_1[i] < min:
                min = burst_time_1[i]
                min_index_arrival = i
                arrival_flag = True
    elif len(list_arrival) == 1:
        min_index_arrival = list_arrival[0]
        arrival_flag = True

    io_flag = False
    min = float('+inf')
    min_index_io_finished = 0
    if len(list_io_finished) > 1:
        for i in range(len(list_io_finished)):  # find minimum burst time in list_io_finished
            if burst_time_2[i] < min:
                min = burst_time_2[i]
                min_index_io_finished = i
                io_flag = True
    elif len(list_io_finished) == 1:
        min_index_io_finished = list_io_finished[0]
        io_flag = True

    if arrival_flag and io_flag:
        if burst_time_1[min_index_arrival] <= burst_time_2[min_index_io_finished]:
            return min_index_arrival
        else:
            return min_index_io_finished
    elif arrival_flag and not io_flag:
        return min_index_arrival
    elif not arrival_flag and io_flag:
        return min_index_io_finished
    else:
        return 0


# this method implement Shortest Job First or 'SJF'
def SJF(arrival_time_o, burst_time_1, io_time, burst_time_2):
    arrival_time = arrival_time_o.copy()
    io_finished_at = list()
    complete_time = list()
    response_time = list()
    status = build_status(arrival_time)
    cpu_time = 0
    for i in range(len(io_time)):
        io_finished_at.append(-1)
        complete_time.append(-1)
    while not is_done(status):
        # find the next process that should execute
        process_turn = next_process_SJF(arrival_time, io_finished_at, burst_time_1, burst_time_2, cpu_time)

        # this condition is true when process want to execute 'cpu time 1'
        if status[process_turn] == 'CP' and arrival_time[process_turn] <= cpu_time:
            temp = cpu_time - arrival_time[process_turn]
            response_time.append(temp)
            cpu_time += burst_time_1[process_turn]
            status[process_turn] = 'IO'
            arrival_time[process_turn] = -1
            io_finished_at[process_turn] = cpu_time + io_time[process_turn]

        # this condition is true when process want to execute 'cpu time 2'
        elif status[process_turn] == 'IO' and io_finished_at[process_turn] <= cpu_time:
            cpu_time += burst_time_2[process_turn]
            status[process_turn] = 'Done'
            io_finished_at[process_turn] = -1
            complete_time[process_turn] = cpu_time
        else:
            cpu_time += 1

    # find turn around time and waiting time with 'calculate_tat_wt' function
    turn_around_time, waiting_time = calculate_tat_wt(arrival_time_o, complete_time, burst_time_1, burst_time_2,
                                                      io_time)

    return arrival_time_o, complete_time, turn_around_time, waiting_time, response_time, cpu_time
