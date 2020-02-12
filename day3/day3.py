import numpy as np

def increment_matrix(mat, path, cur, wire_nb):
  for elt in path.split(','):
    direction = elt[0]
    steps = int(elt[1:])

    if direction == 'R':
      for i in range(1, steps + 1):
        mat[cur[0], cur[1] + i] += wire_nb
      cur[1] += steps
    if direction == 'D':
      for i in range(1, steps + 1):
        mat[cur[0] + i, cur[1]] += wire_nb
      cur[0] += steps
    if direction == 'U':
      for i in range(1, steps + 1):
        mat[cur[0] - i, cur[1]] += wire_nb
      cur[0] -= steps
    if direction == 'L':
      for i in range(1, steps + 1):
        mat[cur[0], cur[1] - i] += wire_nb
      cur[1] -= steps

def find_dist_to_intersection(mat, path, intersection, middle):
  cur = [middle, middle]
  dist_to_intersection = 0

  for elt in path.split(','):
    direction = elt[0]
    steps = int(elt[1:])

    if direction == 'R':
      for i in range(1, steps + 1):
        if cur[0] == intersection[0] and cur[1] == intersection[1]:
          return dist_to_intersection
        else:
          cur[1] +=1
          dist_to_intersection += 1
    if direction == 'D':
      for i in range(1, steps + 1):
        if cur[0] == intersection[0] and cur[1] == intersection[1]:
          return dist_to_intersection
        else:
          cur[0] +=1
          dist_to_intersection += 1
    if direction == 'U':
      for i in range(1, steps + 1):
        if cur[0] == intersection[0] and cur[1] == intersection[1]:
          return dist_to_intersection
        else:
          cur[0] -=1
          dist_to_intersection += 1
    if direction == 'L':
      for i in range(1, steps + 1):
        if cur[0] == intersection[0] and cur[1] == intersection[1]:
          return dist_to_intersection
        else:
          cur[1] -=1
          dist_to_intersection += 1

def main():
  input_name = 'input.txt'
  
  with open(input_name,'r') as file:
    size = 20001 
    middle = int(size / 2)
    mat1 = np.zeros((size, size))
    mat1[middle,middle] = 1
    
    # part1
    for ix, line in enumerate(file):
      current = [middle, middle]
      increment_matrix(mat1, line.strip(), current, ix + 1)

    print('Part1, finding wire intersections.')
    res = np.where(mat1 == 3)
    print(f'{len(res[0])} intersections found.')
    closest = 10000
    for i in range(len(res[0])):
      x_dist = abs(res[0][i] - middle)
      y_dist = abs(res[1][i] - middle)
      tot = x_dist + y_dist
      if tot < closest:
        closest = tot
    print(f'Closest distance : {closest}.')
    file.close()
  
  # part2
  with open(input_name,'r') as file:
    dist_inter_each_wire = []
    
    print('Part2, going through wire intersections.')
    for line in file:
      cur_wire_inter_distances = []
      for i in range(len(res[0])):
        cur_wire_inter_distances.append(find_dist_to_intersection(mat1, line.strip(), [res[0][i], res[1][i]], middle))
      dist_inter_each_wire.append((cur_wire_inter_distances))

    assert(len(dist_inter_each_wire) == 2)

    summed_dist = [0] * len(res[0])
    for elt in dist_inter_each_wire:
      for i in range(len(res[0])):
        summed_dist[i] += elt[i]

    print(min(summed_dist))
    file.close()

main()
