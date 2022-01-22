# this method build the initial status
# this method config all process status on 'CP'
def build_status(arrival_time):
    status = {}
    for i in range(len(arrival_time)):
        status[i] = 'CP'
    return status


# this method check that is all process Done or not
def is_done(status):
    for i in status.values():
        if i != 'Done':
            return False
    return True


# this method calculate turn around time and waiting time with formula below
# turn around time = complete time - arrival time
# waiting time = turn around time - burst time - io time
def calculate_tat_wt(arrival_time_o, complete_time, burst_time_1, burst_time_2, io_time):
    turn_around_time = list()
    waiting_time = list()
    for i in range(len(arrival_time_o)):
        temp = complete_time[i] - arrival_time_o[i]
        turn_around_time.append(temp)
        temp = turn_around_time[i] - (burst_time_1[i] + burst_time_2[i]) - io_time[i]
        waiting_time.append(temp)
    return turn_around_time, waiting_time


# this method use to print output organizationally
def print_output(arrival_time, complete_time, turn_around_time, waiting_time, response_time, total_time, burst_time_1,
                 burst_time_2, print_for):
    lentgh = len(arrival_time)
    total_response = 0
    total_turnaround = 0
    total_waiting = 0
    total_burst_time = 0
    print()
    print()
    print("======================================================================================================")
    print(f"\t\t\t\t\t\t\t\t\t\t\t{print_for}")
    print("======================================================================================================")
    print("\tresponse time\t\tturnaround time\t\twaiting time\t\tarrival time\t\tcomplete time")
    for i in range(lentgh):
        print(
            f"P{i}\t\t{response_time[i]}\t\t\t\t\t{turn_around_time[i]}\t\t\t\t\t{waiting_time[i]}\t\t\t\t\t{arrival_time[i]}\t\t\t\t\t{complete_time[i]}")
        total_response += response_time[i]
        total_turnaround += turn_around_time[i]
        total_waiting += waiting_time[i]
        total_burst_time += burst_time_1[i] + burst_time_2[i]
    print("_______________________________________________________________________________________________________")
    print(f"AVG\t\t{total_response / lentgh}\t\t\t\t\t{total_turnaround / lentgh}\t\t\t\t{total_waiting / lentgh}")
    print()
    print(f"\t\tTotal Time = {total_time}")
    print(f"\t\tIdle Time = {total_time - total_burst_time}")
    print(f"\t\tBurst Time = {total_burst_time}")
    print(f"\t\tUtilization = %{(total_burst_time / total_time) * 100}")
    print(f"\t\tThroughput = {(lentgh * 1000) / total_time}")
