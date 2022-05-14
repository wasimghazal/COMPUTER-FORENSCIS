# ET4027 Laboratory Lab Project PHASE 2
# Author: Wasim Ghazal Aswad
# Due Date: 11/04/2022
# Summary: The programme will do the following:
#1. Displays the number of partitions on the disk 
#   and the type of that partition with its total size.
#2. Read the image "Sample_1.dd" and display the partition
#   number with its type and its start sector, size of the
#   partition, and end sector.
#3. It displays the size of the gap between each partition
#   if it exists.
#4. Also it gave some information about the FAT like (display
#   the number of sectors per cluster, the size of the FAT 
#   area, the size of the Root Directory, and the sector 
#   address of Cluster #2)
#5. It will show the name of the deleted file if it exists.
#6. Finally, it gave some information about the NTFS like:
#a) How many byes per sector for this NTFS volume
#b) How many sectors per cluster for this NTFS volume
#c) What is the sector address for the $MFT file record
#d) What is the type and length of the first two attributes 
#   in the $MFT record.

from __future__ import print_function
import psutil
import shutil
import win32api
import os.path
import binascii

print("\n************************************")
print("* Student Name: Wasim Ghazal Aswad *")
print("* Student ID: 17193559             *")
print("************************************\n")

def drives_details():  # This function is doing getting and show different details about the drives
    drivers = win32api.GetLogicalDriveStrings()
    drivers = drivers.split('\000')[:-1]
    drivers_length = len(drivers)

    dps = psutil.disk_partitions()
    fmt_str = "{:<8} {:<7} {:<23} {:<13} {:<10}"
    print(fmt_str.format("Drive", "Type", "Opts", "Total Size", ""))
    print(fmt_str.format("=====", "----", "--------", "-------------", ""))

    # Only show a couple of different types of devices, for brevity.
    for i in range(9):
        if i == drivers_length:
            break
        dp = dps[i]
        if dp[3] != "cdrom":  # This "if statement" to stop scanning the CD Rom
            stat = shutil.disk_usage(dp[0])
            stat_size = stat[0]
        else:
            stat_size = "Null"
        print(fmt_str.format(dp.device, dp.fstype, dp.opts, stat_size, "Bytes"))


drives_details()
print("\n+++++++++++++++++++++++++++++++++++++++\n")


def reset_list():
    flag_list.clear()
    start_CHS.clear()
    end_CHS.clear()
    start_LBA.clear()
    size.clear()
    empty_list.clear()


# initialize the list of the MBR layout
flag_list = []
start_CHS = []
type_of_partition = []
end_CHS = []
start_LBA = []
size = []
partition_1 = []
partition_2 = []
partition_3 = []
partition_4 = []
empty_list = []


image_file = ""
print("Please enter name of your image file:")
loop_break = True
small_loop = True
while loop_break:
    y_or_n = input("Do you want to use the Sample_1.dd file as an image,\nPlease choose Y/N:")
    if y_or_n == "Y" or y_or_n == "y":
        image_file = "Sample_1.dd"
        loop_break = False
    elif y_or_n == "N" or y_or_n == "n":
        while small_loop:
            image_file = input("Please enter name of your image file:")
            if os.path.isfile(image_file):
                small_loop = False
                loop_break = False
            else:
                print("*** WRONG ENTRY ***")
                print("*** The file does not exist ***")
    else:
        print("*** WRONG ENTRY ***\n")

def read_image(sector, number, bool):
    with open(image_file, "rb") as image:
        image.seek(sector)
        content = image.read(number)
        if not bool:
            return content
        ver = binascii.hexlify(content)
        str_ver = str(ver)
        return str_ver

def split(offset):
    temp = list(offset)
    temp_list = []
    temp_char = ""
    new_char = ""
    for index in range(len(temp)):
        new_char = str(new_char) + str(temp[index])
        if len(new_char) == 2:
            new_char = temp_char + new_char
            temp_list.append(new_char)
            new_char = ""
    temp_list.remove(temp_list[0])
    return temp_list

def convert_hexToDecimal(hex_offset):  # To convert from Hex to Decimal
    return int(hex_offset, 16)

def multiply_operation(input):
    split_list = list(''.join(map(str, input)))  # Divide each byte into bits i.e. (b0) will be (b, 0)
    temp_list = []
    result = 0
    power = len(split_list) - 1  # setting the ace based on the length of the list
    for i in range(0, len(split_list)):
        temp_list.append(convert_hexToDecimal(split_list[i]))  # convert each bit in the list to Decimal number
        temp = temp_list[i] * (16 ** power)  # mathematically => new_list[i] * 16^power
        result = result + temp  # add the answer to the result
        power = power - 1  # new power for new bit
    return result

def operation(offset):
    if isinstance(offset, list):
        big_endian = []
        for i in range(len(offset)):  # To convert the list from (little endian) to (big endian)
            big_endian.insert(0, offset[i])
        return multiply_operation(big_endian)
    elif isinstance(offset, str):
        return multiply_operation(offset)

def typeOfPartition(mypartition):
    temp = mypartition[4]
    if temp == "00":  # check if the bytes = "00"
        return 'Unknown or empty'
    elif temp == "01":  # check if the bytes = "01"
        return '12-bit FAT'
    elif temp == "04":  # check if the bytes = "04"
        return '16-bit FAT'
    elif temp == "05":  # check if the bytes = "05"
        return 'Extended MS-DOS Partition'
    elif temp == "06":  # check if the bytes = "06"
        return 'FAT-16'
    elif temp == "07":  # check if the bytes = "07"
        return 'NTFS'
    elif temp == "0b":  # check if the bytes = "0b"
        return 'FAT-32 (CHS)'
    elif temp == "0C":  # check if the bytes = "0C"
        return 'FAT-32 (LBA)'
    elif temp == "0e":  # check if the bytes = "0e"
        return 'FAT-16 (LBA)'

def start_end(my_partition, operation_name):
    result = []
    if operation_name == "start_CHS":
        for i in range(1, 4):
            result.append(my_partition[i])
    elif operation_name == "end_CHS":
        for i in range(5, 8):
            result.append(my_partition[i])
    elif operation_name == "start_LBA":
        for i in range(8, 12):
            result.append(my_partition[i])
    else:
        for i in range(12, len(my_partition)):
            result.append(my_partition[i])
    answer = operation(result)
    return answer

def flag(my_partition):
    if my_partition[0] == "00":
        return "Inactive / Not bootable"
    elif my_partition[0] == "80":
        return "Active / Bootable"
    else:
        return "Unknown"

def fill_up(my_partition):
    my_list = []
    temp = flag(my_partition)
    my_list.append(temp)
    temp = start_end(my_partition, "start_CHS")
    my_list.append(temp)
    temp = typeOfPartition(my_partition)
    my_list.append(temp)
    temp = start_end(my_partition, "end_CHS")
    my_list.append(temp)
    temp = start_end(my_partition, "start_LBA")
    my_list.append(temp)
    temp = start_end(my_partition, "size")
    my_list.append(temp)
    return my_list


sector_hex = 0x1BE

for i in range(1, 5):
    if i == 1:
        partition = split(read_image(sector_hex, 16, True))
        partition_1 = fill_up(partition)
    elif i == 2:
        partition = split(read_image(sector_hex, 16, True))
        partition_2 = fill_up(partition)
    elif i == 3:
        partition = split(read_image(sector_hex, 16, True))
        partition_3 = fill_up(partition)
    else:
        partition = split(read_image(sector_hex, 16, True))
        partition_4 = fill_up(partition)
    temp_number = sector_hex + int("10", 16)
    sector_hex = temp_number

def add_to_list_partition():
    print("+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+")
    print("+\tPartitions on", image_file, "disk image\t+")
    print("+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+")
    count = 0
    for i in range(1, 5):
        if i == 1:
            print("Partition", i, "\tType:", partition_1[2], "\t\tStart:", partition_1[4], "\tSize: ",
                  partition_1[5], "\tEnd:", partition_1[5]+partition_1[4])
            print("Hidden partition size / Gap size:", (partition_2[4] - (partition_1[5]+partition_1[4])), "\n")
            if partition_1[5] != 0:
                count += 1
        elif i == 2:
            print("Partition", i, "\tType:", partition_2[2], "\tStart:", partition_2[4], "\tSize: ",
                  partition_2[5], "\tEnd:", partition_2[5]+partition_2[4])
            print("Hidden partition size / Gap size:", (partition_3[4] - (partition_2[5]+partition_2[4])), "\n")
            if partition_2[5] != 0:
                count += 1
        elif i == 3:
            print("Partition", i, "\tType:", partition_3[2], "\t\tStart:", partition_3[4], "\tSize: ",
                  partition_3[5], "\tEnd:", partition_3[5]+partition_3[4])
            if partition_3[5] != 0:
                count += 1
        else:
            print("Partition", i, "\tType:", partition_4[2], "\tStart:", partition_4[4], "\tSize: ",
                  partition_4[5], "\tEnd:", partition_4[5]+partition_4[4])
            if partition_4[5] != 0:
                count += 1
            print("\nTotal number of valid partitions is: ", count)


add_to_list_partition()
my_list = split(read_image(0x7E00, 512, True))
print("")
print("---=== FAT16 information ===---")
result = [my_list[17], my_list[18]]
root_size = int((operation(result)*32) / operation(result))
print("Size of Root Directory (Sectors) = \t", root_size)
result.clear()
result = [my_list[14], my_list[15]]
first_sector_volume = operation(result) + convert_hexToDecimal("3f")
print("First sector of FAT Area = \t\t", first_sector_volume)
no_cluster = operation(my_list[13])
print("Number of sectors per cluster = \t", operation(my_list[13]))
result.clear()
result = [my_list[22], my_list[23]]
print("First sector of Data Area = \t\t", first_sector_volume + (operation(result)*2))
Cluster = int(first_sector_volume + (operation(result)*2) + root_size)
print("Cluster #2 location = \t\t\t", Cluster)

print("")
print("---=== Files located in FAT16 partition ===---")
fmt_str = "{:<33} {:<11} {:<18} {:<10}"
print(fmt_str.format("File Name", "Size", "Starting Cluster", "Cluster Sector Address"))
print(fmt_str.format("---------", "----", "----------------", "----------------------"))
sector_hex = 0x46E00
count = 0
delete_file = 0
for i in range(0, 6):
    result.clear()
    my_list = split(read_image(sector_hex, 32, True))
    for index in range(0, 11):
        result.append(my_list[index])
    data = read_image(sector_hex, 11, False)
    temp = str(data)
    if my_list[0] == "e5":
        delete_file += 1
        file_name = "Deleted File Name:" + temp[2:len(temp)-1]
    else:
        count += 1
        file_name = temp[2:len(temp)-1]
    result.clear()
    for index in range(28, len(my_list)):
        result.append(my_list[index])
    size = operation(result)
    result.clear()
    for index in range(26, 28):
        result.append(my_list[index])
    starting_cluster = operation(result)
    temp_number = sector_hex + int("20", 16)
    sector_hex = temp_number
    empty_ = Cluster + ((starting_cluster - 2) * no_cluster)
    print(fmt_str.format(file_name, size, starting_cluster, empty_))

print("")
print("Total files recovered:", count)
print("Total deleted files recovered:", delete_file)
print("")
print("---=== NTFS support information ===---")
my_list = split(read_image(0x3C4D7400, 512, True))
data = [my_list[11], my_list[12]]
answer = operation(data)
print("Number of bytes per sector of a NTFS volume:\t", answer)
data = my_list[13]
answer = operation(data)
print("Number of sectors per cluster of a NTFS volume:\t", answer)
data = []
for index in range(48, 56):
    data.append(my_list[index])
answer = operation(data)
print("The sector address for the $MFT file record:\t", answer)
data.clear()
my_list.clear()
my_list = split(read_image(0x31070800, 512, True))
for index in range(56, 60):
    data.append(my_list[index])
answer = operation(data)
data.clear()
for index in range(60, 64):
    data.append(my_list[index])
length = operation(data)
print("The type and length of the first two attributes in the $MFT record")
print("First attribute: \t Type:", answer, "\tlength:", length)
data.clear()
for index in range(152, 156):
    data.append(my_list[index])
answer = operation(data)
data.clear()
for index in range(156, 160):
    data.append(my_list[index])
length = operation(data)
print("Second attribute: \t Type:", answer, "\tlength:", length, "\n\n")
print("\t\t ====== END ====== \n\n")
