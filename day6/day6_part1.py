import copy
amount_orbits = []

class Node:
  def __init__(self, name, lvl):
    self.children = []
    self.name = name
    self.depth = lvl

  def print_node(self):
    print(f'{self.name} has depth {self.depth} and {len(self.children)} children')

  def insert_node(self, node):
    self.children.append(node)

  def print_tree(self):
    amount_children = len(self.children)
    self.print_node()
    for child in self.children:
      child.print_tree()

  def set_up_tree(self, name_s, raw_input):
    for elt in raw_input:
      if elt[0] == name_s:
        new_node = Node(elt[1], self.depth + 1)
        self.insert_node(new_node)
        new_node.set_up_tree(elt[1], raw_input)

  # Once you realise that the amount of paths is just 
  # the sum of the distances from the first node the problem
  # is easy to solve by just adding each distance to a global variable.
  # Not pretty but works. 
  def calculate_distance(self):
    for child in self.children:
      child.calculate_distance()
    amount_orbits.append(self.depth)

def main():
  with open('input.txt','r') as file:
    raw_input = []
    for line in file:
      raw_line = line.strip().split(')')
      raw_input.append(raw_line)

  root = Node('COM', 0)
  root.set_up_tree('COM', raw_input)
  root.calculate_distance()

  print(f'Total amount of paths is {sum(amount_orbits)}')

main()
