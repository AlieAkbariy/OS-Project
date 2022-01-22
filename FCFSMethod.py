from SharedMethod import build_status, is_done, calculate_tat_wt


def find_minimum_arrival_time(arrival_time):
    index = 0
    min = float('+inf')
    for i in range(len(arrival_time)):
        if arrival_time[i] < min and arrival_time[i] != -1:
            min = arrival_time[i]
            index = i
    return min, index


# this function find the next process index that should execute in 'FCFS algorithm'
def find_next_process(arrival_time, io_finished_at):
    arrival_min, arrival_index = find_minimum_arrival_time(arrival_time)
    io_min, io_index = find_minimum_arrival_time(io_finished_at)
    if arrival_min > io_min:
        return io_index
    else:
        return arrival_index


# this method implement First Come First Serve or 'FCFS'
def FCFS(arrival_time_o, burst_time_1, io_time, burst_time_2):
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
        process_turn = find_next_process(arrival_time, io_finished_at)  # find the next process that should execute

        # this condition is true when process want to execute 'cpu time 1'
        if status[process_turn] == 'CP' and arrival_time[process_turn] <= cpu_time:
            temp = cpu_time - arrival_time[process_turn]
            response_time.append(temp)
            cpu_time += burst_time_1[process_turn]
            status[process_turn] = 'IO'  # change status to 'IO Operation'
            arrival_time[process_turn] = -1
            io_finished_at[process_turn] = cpu_time + io_time[process_turn]

        # this condition is true when process want to execute 'cpu time 2'
        elif status[process_turn] == 'IO' and io_finished_at[process_turn] <= cpu_time:
            cpu_time += burst_time_2[process_turn]
            status[process_turn] = 'Done'  # change status to 'Done'
            io_finished_at[process_turn] = -1
            complete_time[process_turn] = cpu_time
        else:
            cpu_time += 1

    # find turn around time and waiting time with 'calculate_tat_wt' function
    turn_around_time, waiting_time = calculate_tat_wt(arrival_time_o, complete_time, burst_time_1, burst_time_2,
                                                      io_time)

    return arrival_time_o, complete_time, turn_around_time, waiting_time, response_time, cpu_time
