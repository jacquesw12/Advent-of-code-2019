import copy
import itertools

def execute_prg(program):
  # List with indexes of opcodes.
  idx_list = [4*x for x in range(0, int(len(program) / 4))]
  for ix in idx_list:
    opcode = program[ix]
    if opcode == 99:
      break

    nb1 = program[ix + 1]
    nb2 = program[ix + 2]
    pos = program[ix + 3]
    prg_res = 0
    
    if opcode == 1:
      prg_res = program[nb1] + program[nb2]
    elif opcode == 2:
      prg_res = program[nb1] * program[nb2]
    else:
      raise ValueError('Opcode is not defined. The cursor could be pointing to the wrong digit or the input corrupted.')
      break

    program[pos] = prg_res 
  return program[0]


def main():
  with open('input_day_2.txt','r') as file:
    init_prgr = file.read().strip().split(',')
    prgr = [int(elt) for elt in init_prgr]

    # 1st task
    prgr_first_part = copy.deepcopy(prgr)
    prgr_first_part[1] = 12
    prgr_first_part[2] = 2 
    print(execute_prg(prgr_first_part))

    # 2nd task
    for numb1, numb2 in itertools.product(range(0,100), range(0,100)):
      prgr_second_part = copy.deepcopy(prgr) 
      prgr_second_part[1] = numb1
      prgr_second_part[2] = numb2
      result = execute_prg(prgr_second_part)
      if result == 19690720:
        print(100 * numb1 + numb2)
        break

main()
