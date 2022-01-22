import csv


def open_file_input(path):
    file = open(path)
    csv_reader = csv.reader(file)
    return csv_reader


def organize_input(csv_reader):
    next(csv_reader)
    arrival_time = list()
    io_time = list()
    burst_time_1 = list()
    burst_time_2 = list()
    for row in csv_reader:
        arrival_time.append(int(row[1]))
        burst_time_1.append(int(row[2]))
        io_time.append(int(row[3]))
        burst_time_2.append(int(row[4]))

    return arrival_time, burst_time_1, io_time, burst_time_2
