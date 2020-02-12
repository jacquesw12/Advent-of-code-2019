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
  def __init__(self, prg, cur_pos, runs, inp, out_sig):
    self.prg = prg
    self.cur_pos = cur_pos
    self.is_running = runs
    self.inputs = inp #keep track about what input to read in
    self.output_signal = out_sig

  def find_numb_from_mode(self, cur_pos, mode):
    numb = 0
    if mode == 0:
      numb = self.prg[self.prg[cur_pos]]
    if mode == 1:
      numb = self.prg[cur_pos]
    return numb

  def add_input_signal(self, input_signal):
    self.inputs.append(input_signal)
  
  def run_prg_on_amplifier(self):
    continue_ = True
    while(continue_):
      continue_ = self.read_instruction()
    return self.output_signal

  # Returns false when program should terminate (opcode 99)
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

      self.prg[self.prg[self.cur_pos + 3]] = numb1 + numb2
      self.cur_pos += 4

    elif opcode == 2:
      numb1 = self.find_numb_from_mode(self.cur_pos + 1, mode1)
      numb2 = self.find_numb_from_mode(self.cur_pos + 2, mode2)
      
      self.prg[self.prg[self.cur_pos + 3]] = numb1 * numb2
      self.cur_pos += 4

    elif opcode == 3:
      self.prg[self.prg[self.cur_pos + 1]] = self.inputs[0]
      self.inputs.pop(0)
      self.cur_pos += 2

    elif opcode == 4:
      self.output_signal = self.find_numb_from_mode(self.cur_pos + 1, mode1)
      self.cur_pos += 2
      return False

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
      if numb1 < numb2:
        self.prg[self.prg[self.cur_pos + 3]] = 1
      else:
        self.prg[self.prg[self.cur_pos + 3]] = 0
      self.cur_pos += 4

    elif opcode == 8:
      numb1 = self.find_numb_from_mode(self.cur_pos + 1, mode1)
      numb2 = self.find_numb_from_mode(self.cur_pos + 2, mode2)
      numb3 = self.find_numb_from_mode(self.cur_pos + 3, mode3)
      if numb1 == numb2:
        self.prg[self.prg[self.cur_pos + 3]] = 1
      else:
        self.prg[self.prg[self.cur_pos + 3]] = 0
      self.cur_pos += 4

    else:
      raise ValueError('Opcode is not defined. The cursor could be pointing to the wrong digit or the input corrupted.')
    return True

def main():
  # Part 1
  with open('input.txt','r') as file:
    program = file.read().strip().split(',')
    prg = [int(elt) for elt in program] 
    
    list_inputs = generate_possible_inputs([0,1,2,3,4], 1234, 43211) 
    assert(len(list_inputs) == 120)
    max_thrust_signal = 0

    for cur_inp in list_inputs:
      output = 0
      for phase_setting in cur_inp:
        amplifier = Amplifier(copy.deepcopy(prg), 0, True, [phase_setting, output], 0)
        output = amplifier.run_prg_on_amplifier()
      if output > max_thrust_signal:
        max_thrust_signal = output
    print(f'Max thrust part1 : {max_thrust_signal}')
    file.close()

  # Part 2 
  with open('input.txt','r') as file:
    program = file.read().strip().split(',')
    prg = [int(elt) for elt in program] 

    list_inputs = generate_possible_inputs([5,6,7,8,9], 56789, 98765)
    assert(len(list_inputs) == 120)
    max_thrust_signal_part2 = 0
    
    for cur_inp in list_inputs:
      amplifierA = Amplifier(copy.deepcopy(prg), 0, True, [cur_inp[0], 0], 0)
      out_initA = amplifierA.run_prg_on_amplifier()
      amplifierB = Amplifier(copy.deepcopy(prg), 0, True, [cur_inp[1], out_initA], 0)
      out_initB = amplifierB.run_prg_on_amplifier()
      amplifierC = Amplifier(copy.deepcopy(prg), 0, True, [cur_inp[2], out_initB], 0)
      out_initC = amplifierC.run_prg_on_amplifier()
      amplifierD = Amplifier(copy.deepcopy(prg), 0, True, [cur_inp[3], out_initC], 0)
      out_initD = amplifierD.run_prg_on_amplifier()
      amplifierE = Amplifier(copy.deepcopy(prg), 0, True, [cur_inp[4], out_initD], 0)
      out_initE = amplifierE.run_prg_on_amplifier()
      
      continue_ = True
      output = out_initE
      previous_ampE_out = 0

      while(continue_):
        amplifierA.add_input_signal(output)
        output = amplifierA.run_prg_on_amplifier()

        if not amplifierA.is_running:
          continue_ = False
          if previous_ampE_out > max_thrust_signal_part2:
            max_thrust_signal_part2 = previous_ampE_out
        
        amplifierB.add_input_signal(output)
        output = amplifierB.run_prg_on_amplifier()
        amplifierC.add_input_signal(output)
        output = amplifierC.run_prg_on_amplifier()
        amplifierD.add_input_signal(output)
        output = amplifierD.run_prg_on_amplifier()
        amplifierE.add_input_signal(output)
        output = amplifierE.run_prg_on_amplifier()
        previous_ampE_out = output
    
    print(f'Max thrust part2 : {max_thrust_signal_part2}')

main()
