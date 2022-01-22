from FCFSMethod import FCFS
from FileOperation import open_file_input, organize_input
from MLFQMethod import MLFQ
from RRMethod import RR
from SJFMethod import SJF
from SharedMethod import print_output


def main():
    path = 'Data/proces_inputs.csv'
    csv_reader = open_file_input(path)

    arrival_time, burst_time_1, io_time, burst_time_2 = organize_input(csv_reader)

    i = FCFS(arrival_time, burst_time_1, io_time, burst_time_2)
    print_output(i[0], i[1], i[2], i[3], i[4], i[5], burst_time_1, burst_time_2, 'FCFS')

    i = RR(arrival_time, burst_time_1, io_time, burst_time_2)
    print_output(i[0], i[1], i[2], i[3], i[4], i[5], burst_time_1, burst_time_2, 'RR')

    i = SJF(arrival_time, burst_time_1, io_time, burst_time_2)
    print_output(i[0], i[1], i[2], i[3], i[4], i[5], burst_time_1, burst_time_2, 'SJF')

    i = MLFQ(arrival_time, burst_time_1, io_time, burst_time_2)
    print_output(i[0], i[1], i[2], i[3], i[4], i[5], burst_time_1, burst_time_2, 'MLFQ')


if __name__ == '__main__':
    main()
