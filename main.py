import sys
from pathlib import Path

def print_help():
    print(
"""Usage: chind [File] 
    Optional:
        [   Target indentation N :int  (default=4)]
        [-o Output file path     :File (default=overwrite input file)]
        [-f Forced]
"""
    )

if ("-h" or "--help") in sys.argv\
    or len(sys.argv) <= 1:
    print_help()
    quit()

prog, f_name, *args = sys.argv

f_name = Path(f_name)

if "-o" in args:
    idx = args.index("-o")
    o = Path(args[idx+1])
    args.pop(idx)
    args.pop(idx)
else:
    o = f_name

forced = False
for idx, i in enumerate(args.copy()):
    if "-" in i:
        if "f" in i:
            forced = True
            args.pop(idx)

for i in args:
    if "-" in i:
        raise(RuntimeError(f"Unknow option: {i[1:]}"))

chind_to = 4
if len(args) == 0:
    pass
elif args[0].isdigit():
    chind_to = int(args[0])
elif args[0][0] == "-":
    pass
else:
    print_help()
    raise(RuntimeError(f"{{target indentation N}} shoud be a Integer, but got `{args[0]}`{type(args[0])}"))

line_space_table = {}
with open(f_name, 'r') as f:
    lines = f.readlines()

for n_l, l in enumerate(lines):
    num_space = 0
    for chr in l:
        if chr == " ": num_space += 1
        else: break
    if num_space != 0:
        line_space_table[n_l] = num_space
    # print(f'{n_l+1}: {num_space}')

assumed_ind_err_table = {i: 0 for i in range(2, 6)[::-1]}

for indent in assumed_ind_err_table.keys():
    for v in line_space_table.values():
        if v % indent != 0:
            assumed_ind_err_table[indent] += 1
    
assumed_ind = min(assumed_ind_err_table, key=lambda k: assumed_ind_err_table[k])

if not forced:
    u_in = input(f'assumed_ind: {assumed_ind}, conver ot {chind_to}. continue? [Y/n] ')
    if len(u_in) == 0 or u_in.lower() == 'y':
        pass
    else:
        print("Canceled.")
        quit()

for n_l, l in enumerate(lines):
    if n_l not in line_space_table:
        continue

    num_space = line_space_table[n_l]
    # print(num_space)
    indentation = ' ' * num_space
    if num_space % assumed_ind == 0:
        num_ind = num_space // assumed_ind
        indentation = ' ' * chind_to * num_ind

    lines[n_l] = indentation + l[num_space::]

with open(o, 'w') as f:
    for l in lines:
        f.write(l)
            
print("Succeed.")
