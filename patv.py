# Authors:
#   Daniel Pereira Ferragut - 169488
#   Lucas Koiti Geminiani Tamanaha - 182579
import sys
import os
import struct
import resource


def main():
    # Initial Variables
    argv = sys.argv
    pid = argv[1]
    # Getting the exact paths to /proc/[pid] with os.path.join, 'just in case'...
    proc_pid_path = os.path.join('/proc', pid)
    maps_path = os.path.join(proc_pid_path, 'maps')
    pagemap_path = os.path.join(proc_pid_path, 'pagemap')
    valid_ranges = []
    maps_line_list = []

    # Get all the lines in map
    try:
        maps_line_list = [line.rstrip('\n') for line in open(maps_path)]
    except FileNotFoundError:
        print("Process is not listed in /proc")
        return

    # Getting virtual address range from /proc/[pid]/maps
    page_size = resource.getpagesize()
    for i, line in enumerate(maps_line_list):
        maps_line_list[i] = line.split()
        mem_range = maps_line_list[i][0]
        start, end = mem_range.split(sep='-')
        # We get the exact start of a page  dividing its Vddr by the OS's page size
        start = int(start, 16)//page_size
        end = int(end, 16)//page_size
        valid_ranges.append((start, end))

    # For each range found, for each map in this range, find its page table entry
    present = 0
    not_present = 0
    pages_in_ram = []
    pages_not_in_ram = []
    page_table_entry_size = 8
    for virtual_range in valid_ranges:
        start = virtual_range[0]
        end = virtual_range[1]
        current = start
        while current != end:

            # In some specific Linux Kernels, there is a page dedicated to [vsyscall]
            # This page has a quite irregular virtual address that or:
            # 1: Leads to some thrash Page Table Entries
            # 2: Leads to nowhere, effectively breaking the code
            # Therefore, it was chosen to ignore this page ("0xffffffffff600") as it's very problematic
            if current == 0xffffffffff600:
                current += 1
                not_present += 1
                continue

            # read_entry takes the offset of the Vaddr
            # We already divided Vaddr by the page size
            # Now we just multiply by the page table entry size(should always be 8 bytes)
            entry = read_entry(pagemap_path, current * page_table_entry_size)
            pfn = get_pfn(entry)

            if is_present(entry):
                pages_in_ram.append((current, pfn, entry))
                present += 1
            else:
                pages_not_in_ram.append((current, pfn, entry))
                not_present += 1
            current += 1

    print("PID: {}".format(pid))
    print("Total number of pages found: {}".format(present+not_present))
    print("Pages that are in RAM: {}".format(present))
    print("Pages that are not in RAM: {}".format(not_present))
    print("Estimated RAM usage: {} KB".format(present*4))
    print("Estimated TOTAL usage: {} KB".format((present+not_present+1) * 4))
    print("=================== Pages that are not in RAM [{}]===================".format(not_present))
    for i,page in enumerate(pages_not_in_ram):
        print_page(page, i)
    print("=================== Pages in RAM [{}]===================".format(present))
    for i,page in enumerate(pages_in_ram):
        print_page(page, i)


# Helper functions down below
# Some of these helper functions were inspired by https://bit.ly/33WyIQn

# Given a path to the /proc/[pid]/maps and a offset (and page table entry size)
# read_entry seeks the files, finds its bytes
# and retuns
def read_entry(path, offset, size=8):
    with open(path, 'rb') as f:
        f.seek(offset, 0)
        pagemap_value = struct.unpack('Q', f.read(size))[0]
        return pagemap_value


# Gets bits from 0 to 54
def get_pfn(entry):
    return entry & 0x007FFFFFFFFFFFFF


# 63 bit of PTE checks for RAM
def is_present(entry):
    return (entry & (1 << 63)) != 0


# Prints relevant info about a Vaddr
def print_page(page, i):
    vaddr = to_hex(page[0] * 4096, 12)
    pfn = hex(page[1])
    entry = to_hex(page[2], 16)
    print("{}. Virtual addr = {} || Page Table Entry = {} || Page Frame Number = {} ".format(i+1, vaddr, entry, pfn))


# Guarantee that a hex number will have the zeros on the right
def to_hex(num, width):
    num = hex(num)[2:]
    if len(num) > width:
        print("ERROR-HEXOVERLOAD")
    return "0x" + num.zfill(width)


if __name__ == '__main__':
    main()
