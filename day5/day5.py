import sys

def number_to_list(number):
  number_s = str(number)
  digit_list = []
  for elt in number_s:
    digit_list.append(int(elt))
  while len(digit_list) < 5:
    digit_list.insert(0,0)
  assert(len(digit_list) == 5)
  return digit_list

def find_numb_from_mode(prg, cur_pos, mode):
  numb = 0
  if mode == 0:
    numb = prg[prg[cur_pos ]]
  if mode == 1:
    numb = prg[cur_pos]
  return numb

def execute_instruction(code, prg, cur_pos):
  digit_list = number_to_list(code)
  opcode = 10 * digit_list[3] + digit_list[4]
  mode1 = digit_list[2]
  mode2 = digit_list[1]
  mode3 = digit_list[0]
  output = -999

  if opcode == 1:
    numb1 = find_numb_from_mode(prg, cur_pos + 1, mode1)
    numb2 = find_numb_from_mode(prg, cur_pos + 2, mode2)

    prg[prg[cur_pos + 3]] = numb1 + numb2
    cur_pos += 4
    return (output, cur_pos)

  elif opcode == 2:
    numb1 = find_numb_from_mode(prg, cur_pos + 1, mode1)
    numb2 = find_numb_from_mode(prg, cur_pos + 2, mode2)
    
    prg[prg[cur_pos + 3]] = numb1 * numb2
    cur_pos += 4
    return (output, cur_pos)

  elif opcode == 4:
    if mode1 == 0:
      output = prg[prg[cur_pos + 1]]
      # print(f'Output : {prg[prg[cur_pos + 1]]}')
    if mode1 == 1:
      output = prg[cur_pos + 1]
      # print(f'Output : {prg[cur_pos + 1]}')
    cur_pos += 2
    return (output, cur_pos)

  elif opcode == 5:
    numb1 = find_numb_from_mode(prg, cur_pos + 1, mode1)
    numb2 = find_numb_from_mode(prg, cur_pos + 2, mode2)

    if numb1 == 0:
      cur_pos +=3
      return (output, cur_pos)
    else:
      cur_pos = numb2
      return (output, cur_pos)
      
  elif opcode == 6:
    numb1 = find_numb_from_mode(prg, cur_pos + 1, mode1)
    numb2 = find_numb_from_mode(prg, cur_pos + 2, mode2)

    if numb1 == 0:
      cur_pos = numb2
      return (output, cur_pos)
    else:
      cur_pos +=3
      return (output, cur_pos)

  elif opcode == 7:
    numb1 = find_numb_from_mode(prg, cur_pos + 1, mode1)
    numb2 = find_numb_from_mode(prg, cur_pos + 2, mode2)

    if numb1 < numb2:
      prg[prg[cur_pos + 3]] = 1
    else:
      prg[prg[cur_pos + 3]] = 0

    cur_pos += 4
    return (output, cur_pos)

  elif opcode == 8:
    numb1 = find_numb_from_mode(prg, cur_pos + 1, mode1)
    numb2 = find_numb_from_mode(prg, cur_pos + 2, mode2)

    if numb1 == numb2:
      prg[prg[cur_pos + 3]] = 1
    else:
      prg[prg[cur_pos + 3]] = 0

    cur_pos += 4
    return (output, cur_pos)

  else:
    raise ValueError('Opcode is not defined. The cursor could be pointing to the wrong digit or the input corrupted.')

def solve_problem(problem_input):
  with open('input.txt','r') as file:
    program = file.read().strip().split(',')
    prg = [int(elt) for elt in program] 
    prg_input = problem_input
    cur_pos = 0
    continue_ = True

    while(continue_):
      if prg[cur_pos] == 99:
        continue_= False
      elif prg[cur_pos] == 3:
        prg[prg[cur_pos + 1]] = prg_input
        cur_pos += 2
      else:
        output, cur_pos = execute_instruction(prg[cur_pos], prg, cur_pos)

    return output

def main():
  output = solve_problem(1)
  print(f'Output part 1 : {output}')
  output = solve_problem(5)
  print(f'Output part 2 : {output}')

main()
