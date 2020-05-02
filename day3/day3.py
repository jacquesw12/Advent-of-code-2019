import numpy as np

def increment_matrix(mat, path, middle, wire_nb):
  cur = [middle, middle]
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

def go_through_intersection(mat, path, intersection, middle):
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

def initialise_matrix():
    size = 20001
    center = int(size / 2)
    mat1 = np.zeros((size, size))
    mat1[center, center] = 1
    return mat1, center

def main():
  input_name = 'input.txt'

  with open(input_name,'r') as file:
    mat1, matrix_center = initialise_matrix()

    # part1
    for ix, line in enumerate(file):
      increment_matrix(mat1, line.strip(), matrix_center, ix + 1)

    print('finding intersections')
    res = np.where(mat1 == 3)
    amount_intersections = len(res[0])
    print(f'{amount_intersections} intersections found')
    closest = 10000

    for i in range(amount_intersections):
      x_dist = abs(res[0][i] - matrix_center)
      y_dist = abs(res[1][i] - matrix_center)
      tot = x_dist + y_dist
      if tot < closest:
        closest = tot
    print(f'Closest distance : {closest}')
    file.close()

  # part2
  with open(input_name,'r') as file:
    tot_dist = []

    for line in file:
      cur_line_inter_dist = []
      for i in range(amount_intersections):
        cur_line_inter_dist.append(go_through_intersection(mat1, line.strip(), [res[0][i], res[1][i]], matrix_center))
      tot_dist.append((cur_line_inter_dist))
 
    combined_dist_to_intersection = [0] * amount_intersections 
    for elt in tot_dist:
      for i in range(amount_intersections):
        combined_dist_to_intersection[i] += elt[i]

    print(f'Fewest combined steps {min(combined_dist_to_intersection)}')
    file.close()

main()
