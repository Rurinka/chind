import sys

prog, f_name, *args = sys.argv

# print(f_name)
# print(args)
chind_to = 4

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

# for i in lines:
    # print(i)
print(f'assumed_ind: {assumed_ind}')

with open(f_name, 'w') as f:
    for l in lines:
        f.write(l)
            
