import sys
import os
import struct
from tqdm import tqdm


# TODO: ERRO MUITO PROVAVELMENTE EM COMO PYTHON 3 faz f.read
# Entry sao os 64 bits do pagemap
# Diferencas entre o nosso e esperado: Os bytes finais
# Nosso:    0x8180000000000000
# Esperado: 0x818000000021367f
# Acho que é problema do read mesmo, talvez depende do sistema
def read_entry(path, offset, size=8):
    with open(path, 'rb') as f:
        f.seek(offset, 0)
        try:
            pagemap_value = struct.unpack('Q', f.read(size))[0]
        except struct.error:
            return 'EOF'
        return pagemap_value


def main():
    # Variaveis iniciais
    argv = sys.argv
    pid = argv[1]
    proc_pid_path = os.path.join('/proc', pid)
    maps_path = os.path.join(proc_pid_path, 'maps')
    pagemap_path = os.path.join(proc_pid_path, 'pagemap')
    valid_ranges = []
    maps_line_list = []
    entry_list = []
    try:
        maps_line_list = [line.rstrip('\n') for line in open(maps_path)]
    except:
        print("Process is not listed in /proc")

    for i, line in enumerate(maps_line_list):
        maps_line_list[i] = line.split()
        # if line[4] != '0':
        mem_range = maps_line_list[i][0]
        start, end = mem_range.split(sep='-')
        start = start[:-3]
        end = end[:-3]
        # print(start, end)
        valid_ranges.append((start, end))

    i = 0
    present = 0
    not_present = 0
    for virtual_range in tqdm(valid_ranges):
        start = int(virtual_range[0], 16)
        end = int(virtual_range[1], 16)
        current = start
        while current != end:
            # Offset seria vaddr/page_size * page map entry
            # Mas já tirei os 3 ultimos digitos (dividir por 4096) e multipliquei por 8 (entrada no pagemaps tem 8 bytes)
            entry = read_entry(pagemap_path, current * 8)
            if entry == 'EOF':
                break
            pfn = get_pfn(entry)

            if is_present(entry):
                present += 1
            else:
                not_present += 1

            # print("Vaddr =  {} Offset = {} Entry: {}".format(hex(current*4096), hex(current*8), hex(entry)))
            # print("Is Present? : {}".format(is_present(entry)))
            # print("Is file-page: {}".format(is_file_page(entry)))
            # print("Page count: {}".format(get_pagecount(pfn)))
            # print("Page flags: {}".format(hex(get_page_flags(pfn))))
            current += 1
    print("Presentes: ", present)
    print("Não presentes: ", not_present)


def get_pfn(entry):
    return entry & 0x7FFFFFFFFFFFFF


def is_present(entry):
    return (entry & (1 << 63)) != 0


if __name__ == '__main__':
    main()
