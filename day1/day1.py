def part_one():
  total = 0
  with open('input_day_1.txt', 'r') as file:
    for line in file:
      numb = int(line.strip())
      numb = int(numb / 3) - 2
      total += numb 
  print(total) 

def calculate_total_fuel(wght):
  fuel = int(wght / 3) - 2
  total_fuel = fuel
  while fuel > 0:
    fuel = int(fuel / 3) - 2 
    if fuel > 0:
      total_fuel += fuel
  return total_fuel

def part_two():
  with open('input_day_1.txt', 'r') as file:
    tot = 0
    for line in file:
      wght = int(line.strip())
      module_fuel = calculate_total_fuel(wght)
      tot += module_fuel
    print(tot)

def main():
  part_one()
  part_two()

main()
