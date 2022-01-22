from FCFSMethod import find_next_process
from RRMethod import next_process_RR
from SharedMethod import build_status, is_done, calculate_tat_wt


def MLFQ(arrival_time_o, burst_time_1_o, io_time, burst_time_2_o):
    burst_time_1 = burst_time_1_o.copy()
    burst_time_2 = burst_time_2_o.copy()
    arrival_time = arrival_time_o.copy()
    io_finished_at = list()
    complete_time = list()
    response_time = list()
    process_list_level_1 = list()
    process_list_level_2 = list()
    process_list_level_3 = list()
    status = build_status(arrival_time)
    cpu_time = 0
    for i in range(len(io_time)):
        io_finished_at.append(-1)
        complete_time.append(-1)
        process_list_level_1.append(i)  # at first all processes are in level 1 queue

    while not is_done(status):
        if len(process_list_level_1) > 0:  # if there is a process in level 1 this block execute
            # block 1 in this multi level feedback queue is Rand Robin with time quantum 8
            i = 0
            while i < len(process_list_level_1):  # try to find next process to execute
                process_list_level_1, process_turn = next_process_RR(process_list_level_1)
                if (arrival_time[process_turn] <= cpu_time and arrival_time[process_turn] != -1) or \
                        (io_finished_at[process_turn] <= cpu_time and io_finished_at[process_turn] != -1):
                    break
                i += 1

            # this condition is true when process want to execute 'cpu time 1'
            if status[process_turn] == 'CP' and arrival_time[process_turn] <= cpu_time and arrival_time[
                process_turn] != -1:
                if burst_time_1[process_turn] <= 8:  # when burst time is lower than time quantum
                    temp = cpu_time - arrival_time[process_turn]
                    response_time.append(temp)
                    cpu_time += burst_time_1[process_turn]
                    burst_time_1[process_turn] = 0
                    status[process_turn] = 'IO'  # change status to 'IO Operation'
                    arrival_time[process_turn] = -1
                    io_finished_at[process_turn] = cpu_time + io_time[process_turn]
                else:  # when burst time is greater than time quantum
                    temp = cpu_time - arrival_time[process_turn]
                    response_time.append(temp)
                    cpu_time += 8
                    burst_time_1[process_turn] -= 8
                    process_list_level_1.pop(process_turn)
                    process_list_level_2.append(process_turn)

            # this condition is true when process want to execute 'cpu time 2'
            elif (status[process_turn] == 'IO' or status[process_turn] == 'CP2') and io_finished_at[
                process_turn] <= cpu_time and io_finished_at[
                process_turn] != -1:
                if burst_time_2[process_turn] <= 8:  # when burst time is lower than time quantum
                    cpu_time += burst_time_2[process_turn]
                    burst_time_2[process_turn] = 0
                    status[process_turn] = 'Done'  # change status to 'Done'
                    io_finished_at[process_turn] = -1
                    complete_time[process_turn] = cpu_time
                else:  # when burst time is greater than time quantum
                    cpu_time += 8
                    burst_time_2[process_turn] -= 8
                    status[process_turn] = 'CP2'  # change status to 'CP2' to execute remaining burst time
                    process_list_level_1.pop(process_turn)
                    process_list_level_2.append(process_turn)
            else:
                cpu_time += 1

        elif len(process_list_level_2) > 0:  # if there is a process in level 2 this block execute
            # block 2 in this multi level feedback queue is Rand Robin with time quantum 16
            i = 0
            while i < len(process_list_level_2):  # try to find next process to execute
                process_list_level_2, process_turn = next_process_RR(process_list_level_2)
                if (arrival_time[process_turn] <= cpu_time and arrival_time[process_turn] != -1) or \
                        (io_finished_at[process_turn] <= cpu_time and io_finished_at[process_turn] != -1):
                    break
                i += 1

            # this condition is true when process want to execute 'cpu time 1'
            if status[process_turn] == 'CP' and arrival_time[process_turn] <= cpu_time and arrival_time[
                process_turn] != -1:
                if burst_time_1[process_turn] <= 16:  # when burst time is lower than time quantum
                    temp = cpu_time - arrival_time[process_turn]
                    response_time.append(temp)
                    cpu_time += burst_time_1[process_turn]
                    burst_time_1[process_turn] = 0
                    status[process_turn] = 'IO'  # change status to 'IO Operation'
                    arrival_time[process_turn] = -1
                    io_finished_at[process_turn] = cpu_time + io_time[process_turn]
                else:  # when burst time is greater than time quantum
                    temp = cpu_time - arrival_time[process_turn]
                    response_time.append(temp)
                    cpu_time += 16
                    burst_time_1[process_turn] -= 16
                    process_list_level_2.pop(process_turn)
                    process_list_level_3.append(process_turn)

            # this condition is true when process want to execute 'cpu time 2'
            elif (status[process_turn] == 'IO' or status[process_turn] == 'CP2') and io_finished_at[
                process_turn] <= cpu_time and io_finished_at[
                process_turn] != -1:
                if burst_time_2[process_turn] <= 16:  # when burst time is lower than time quantum
                    cpu_time += burst_time_2[process_turn]
                    burst_time_2[process_turn] = 0
                    status[process_turn] = 'Done'  # change status to 'Done'
                    io_finished_at[process_turn] = -1
                    complete_time[process_turn] = cpu_time
                else:  # when burst time is greater than time quantum
                    cpu_time += 16
                    burst_time_2[process_turn] -= 16
                    status[process_turn] = 'CP2'  # change status to 'CP2' to execute remaining burst time
                    process_list_level_2.pop(process_turn)
                    process_list_level_3.append(process_turn)
            else:
                cpu_time += 1

        elif len(process_list_level_3) > 0:  # if there is a process in level 3 this block execute
            # block 3 in this multi level feedback queue is First Come First Serve

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
    turn_around_time, waiting_time = calculate_tat_wt(arrival_time_o, complete_time, burst_time_1_o, burst_time_2_o,
                                                      io_time)

    return arrival_time_o, complete_time, turn_around_time, waiting_time, response_time, cpu_time
