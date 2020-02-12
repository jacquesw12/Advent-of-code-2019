def number_to_list(number):
  number_s = str(number)
  digit_list = []
  for elt in number_s:
    digit_list.append(int(elt))
  return digit_list

def is_number_possible(number):
  digit_list = number_to_list(number)
  for ix in range(len(digit_list) - 1):
    if not digit_list[ix] <= digit_list[ix + 1]:
      return False
  for ix in range(len(digit_list) - 1):
    if digit_list[ix] == digit_list[ix + 1]:
      return True
  return False

def fulfill_grouping_criteria(number):
  digit_list = number_to_list(number)

  cur_digit = digit_list[0]
  prev_digit = digit_list[0]
  cur_count = 1
  i = 1

  while i < 6:
    cur_digit = digit_list[i]
    if cur_digit == prev_digit:
      cur_count += 1
    if i == 5 and cur_count ==2:
      return True
    if cur_digit != prev_digit and cur_count == 2:
      return True
    if cur_digit != prev_digit:
      cur_count = 1

    prev_digit = cur_digit
    i += 1
  return False

def main():
  # part1
  count = 0
  for number in range(353096, 843213):
    if is_number_possible(number):
      count += 1
  
  print(f'Part one: {count} matches')

  # part 2
  count2 = 0
  for number in range(353096, 843213):
    if is_number_possible(number) and fulfill_grouping_criteria(number):
      count2 += 1
  print(f'Part two, {count2} matches')

main()
