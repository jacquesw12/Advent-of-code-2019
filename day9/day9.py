import sys
import copy

def number_to_list(number):
  number_s = str(number)
  digit_list = []
  for elt in number_s:
    digit_list.append(int(elt))
  while len(digit_list) < 5:
    digit_list.insert(0,0)
  return digit_list

# Is the current number (in a list) suitable to be an
# input, i.e is only composed of digits from the list
# suitable digits
def is_list_suitable(number_list, suitable_digits):
    for i in suitable_digits:
      if not i in number_list:
        return False
    return True

# Generate all inputs containing only digits from
# vector suitable_digits between numb1 and numb2
def generate_possible_inputs(suitable_digits, numb1, numb2):
  list_inputs = []
  for number in range(numb1, numb2 + 1):
    number_list = number_to_list(number)
    if (is_list_suitable(number_list, suitable_digits)):
      list_inputs.append(number_list)
  return list_inputs

### 
# Amplifier class
###
class Amplifier:
  def __init__(self, prg, cur_pos, rel_base, inp, out_sig):
    self.prg = prg
    self.cur_pos = cur_pos
    self.relative_base = rel_base
    self.inputs = inp #keep track about what input to read in
    self.output_signal = out_sig

  def print_state(self):
    code = self.prg[self.cur_pos]
    digit_list = number_to_list(code)
    opcode = 10 * digit_list[3] + digit_list[4]
    print(f'cur pos : {self.cur_pos}, rel base : {self.relative_base}, cur opcode : {opcode}')
    print(self.prg[:30])

  def find_address_from_mode(self, cur_pos, mode):
    address = 0
    # position mode
    if mode == 0:
      address = self.prg[cur_pos]
    # immediate mode, should not be possible for input
    if mode == 1:
      address = cur_pos
    # relative mode
    if mode == 2:
      address = self.prg[cur_pos] + self.relative_base
    return address 

  def find_numb_from_mode(self, cur_pos, mode):
    numb = 0
    # position mode
    if mode == 0:
      numb = self.prg[self.prg[cur_pos]]
    # immediate mode
    if mode == 1:
      numb = self.prg[cur_pos]
    # relative mode
    if mode == 2:
      numb = self.prg[self.prg[cur_pos] + self.relative_base]
    return numb

  def add_input_signal(self, input_signal):
    self.inputs.append(input_signal)
  
  def run_prg_on_amplifier(self):
    continue_ = True
    while(continue_):
      # self.print_state()
      continue_ = self.read_instruction()
    return self.output_signal

  # or when output is returned for the next amplifier (opcode 4)
  def read_instruction(self):
    code = self.prg[self.cur_pos]
    digit_list = number_to_list(code)
    opcode = 10 * digit_list[3] + digit_list[4]
    mode1 = digit_list[2]
    mode2 = digit_list[1]
    mode3 = digit_list[0]

    if self.prg[self.cur_pos] == 99:
      self.is_running = False
      return False

    if opcode == 1:
      numb1 = self.find_numb_from_mode(self.cur_pos + 1, mode1)
      numb2 = self.find_numb_from_mode(self.cur_pos + 2, mode2)
      address = self.find_address_from_mode(self.cur_pos + 3, mode3)

      self.prg[address] = numb1 + numb2
      self.cur_pos += 4

    elif opcode == 2:
      numb1 = self.find_numb_from_mode(self.cur_pos + 1, mode1)
      numb2 = self.find_numb_from_mode(self.cur_pos + 2, mode2)
      address = self.find_address_from_mode(self.cur_pos + 3, mode3)
      
      self.prg[address] = numb1 * numb2
      self.cur_pos += 4

    elif opcode == 3:
      address = self.find_address_from_mode(self.cur_pos + 1, mode1)
      self.prg[address] = self.inputs[0]
      self.inputs.pop(0)
      self.cur_pos += 2

    elif opcode == 4:
      self.output_signal = self.find_numb_from_mode(self.cur_pos + 1, mode1)
      self.cur_pos += 2

    elif opcode == 5:
      numb1 = self.find_numb_from_mode(self.cur_pos + 1, mode1)
      numb2 = self.find_numb_from_mode(self.cur_pos + 2, mode2)

      if numb1 == 0:
        self.cur_pos +=3
      else:
        self.cur_pos = numb2
        
    elif opcode == 6:
      numb1 = self.find_numb_from_mode(self.cur_pos + 1, mode1)
      numb2 = self.find_numb_from_mode(self.cur_pos + 2, mode2)
      if numb1 == 0:
        self.cur_pos = numb2
      else:
        self.cur_pos +=3

    elif opcode == 7:
      numb1 = self.find_numb_from_mode(self.cur_pos + 1, mode1)
      numb2 = self.find_numb_from_mode(self.cur_pos + 2, mode2)
      address = self.find_address_from_mode(self.cur_pos + 3, mode3)

      if numb1 < numb2:
        self.prg[address] = 1
      else:
        self.prg[address] = 0
      self.cur_pos += 4

    elif opcode == 8:
      numb1 = self.find_numb_from_mode(self.cur_pos + 1, mode1)
      numb2 = self.find_numb_from_mode(self.cur_pos + 2, mode2)
      address = self.find_address_from_mode(self.cur_pos + 3, mode3)

      if numb1 == numb2:
        self.prg[address] = 1
      else:
        self.prg[address] = 0
      self.cur_pos += 4

    elif opcode == 9:
      self.relative_base += self.find_numb_from_mode(self.cur_pos + 1, mode1)
      self.cur_pos += 2
    else:
      raise ValueError('Opcode is not defined. The cursor could be pointing to the wrong digit or the input corrupted.')
    return True

def main():
  # Part 1
  with open('input.txt','r') as file:
    program = file.read().strip().split(',')
    prg = [int(elt) for elt in program] 
    for i in range(0, 1000000):
      prg.append(0)

    amplifier_part1 = Amplifier(copy.deepcopy(prg), 0, 0, [1], 0)
    output = amplifier_part1.run_prg_on_amplifier()
    print(f'Result from part 1: {output}')

    amplifier_part2 = Amplifier(copy.deepcopy(prg), 0, 0, [2], 0)
    output = amplifier_part2.run_prg_on_amplifier()
    print(f'Result from part 2: {output}')
    file.close()



main()
