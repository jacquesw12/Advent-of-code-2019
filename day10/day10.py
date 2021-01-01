import numpy as np
import argparse
import pathlib

from collections import OrderedDict
from math import atan, pi, sqrt

RAD2DEG = 180 / pi

def _existing_file(arg):
    path = pathlib.Path(arg)
    if path.is_file():
        return path
    raise argparse.ArgumentTypeError(f'Invalid file: {arg}')

def _get_args():
    """Returns the cli arguments for this application."""
    parser = argparse.ArgumentParser(
        prog='My solution to Advent of code 2019, day 10\n',
        epilog=f'Written by Jacques Wild.\n'
    )   

    parser.add_argument(
        '-v', '--verbose', default=False, help = 'More debug printouts'
    )

    parser.add_argument(
        '-i', '--input', required = True, type = _existing_file, 
        help = 'Path to problem input'
    )

    args = parser.parse_args()
    return args

def create_matrix(file, mat):
  file.seek(0)
  for ix_line,line in enumerate(file):
    for ix_col,char in enumerate(line):
      if char == '.':
        mat[ix_line, ix_col] = 0
      if char == '#':
        mat[ix_line, ix_col] = 1

def init_matrix(file):
  nb_lines = 0
  nb_columns = 0
  for line in file:
    nb_lines += 1
  file.seek(0)
  for line in file.readlines():
    line = line.strip()
    for char in line:
      nb_columns += 1
    break
  return np.empty((nb_lines, nb_columns,))

def input_to_np_matrix(file):
  nb_lines = 0
  nb_columns = 0
  for line in file:
    nb_lines += 1
  file.seek(0)
  for line in file.readlines():
    line = line.strip()
    for char in line:
      nb_columns += 1
    break

  mat = np.empty((nb_lines, nb_columns,))
  
  file.seek(0)
  for ix_line,line in enumerate(file):
    for ix_col,char in enumerate(line):
      if char == '.':
        mat[ix_line, ix_col] = 0
      if char == '#':
        mat[ix_line, ix_col] = 1

  all_ast = np.nonzero(mat)
  asteroids_loc = []
  for i in range(len(all_ast[0])):
    asteroids_loc.append((all_ast[0][i], all_ast[1][i]))

  return mat

def calculate_direction_vector(ast1, ast2):
    return [coor1 - coor2 for coor1, coor2 in zip(ast1, ast2)]

def cross_product(vec1, vec2):
    return vec1[0] * vec2[1] - vec2[0] * vec1[1]

def dot_product(vec1, vec2):
    return vec1[0] * vec2[0] + vec1[1] * vec2[1]

def is_colinear(cur_dir_vector, direction_vector_list):
    if cur_dir_vector == [0,0]:
        return False
    for dir_vector in direction_vector_list:
        if cross_product(cur_dir_vector, dir_vector) == 0 and dot_product(cur_dir_vector, dir_vector) > 0:
            return True
    direction_vector_list.append(cur_dir_vector) 
    return False


class Asteroid:
  def __init__(self, x_, y_):
      self.x = x_
      self.y = y_
      self.angle = -1
      self.distance = -1
  
  def __repr__(self):
      return (
        f'(x : {self.x}, ' 
        f'y : {self.y}, '
        f'theta : {self.angle:.1f}, '
        f'dist : {self.distance:.1f})'
      )

  def calculate_direction_vector(self, ast):
      return [self.x - ast.x, self.y - ast.y]

  def angle_with(self, laser_ast):
      x, y = self.calculate_direction_vector(laser_ast)
      if x < 0: 
          self.angle = -(atan(y / x)) * RAD2DEG % 360
      if x > 0: 
          self.angle = (-atan(y / x) + pi ) * RAD2DEG
      if x == 0 and y > 0:
          self.angle = pi / 2 * RAD2DEG
      if x == 0 and y < 0:
          self.angle = 3 * pi / 2 * RAD2DEG


def get_ix_next(asteroids, condition, verbose):
  asts_at_angle = []
  for ix, ast in enumerate(asteroids):
    if condition(ast) == True:
        asts_at_angle.append((ix, ast))
  
  if not asts_at_angle:
    raise ValueError('No asteroid at current angle found')
  
  min_dist = asts_at_angle[0][1].distance
  ix_min_dist = asts_at_angle[0][0]

  for pair in asts_at_angle:
      if pair[1].distance < min_dist:
          min_dist = pair[1].distance
          ix_min_dist = pair[0]
  
  if verbose:  
      print(asts_at_angle)
      print(f'Remove ast dist {min_dist}, ix {ix_min_dist}')

  return ix_min_dist

def vaporise_next_asteroid(cur_angle, asteroids, verbose):
  next_ix = get_ix_next(asteroids, lambda x : x.angle == cur_angle, verbose)
  if next_ix == -1:
    raise ValueError('Requested angle not found in asteroid list')
  return(asteroids.pop(next_ix))


class Universe:
  def __init__(self, ast_list, base_ast):
    self.asteroids = ast_list
    self.base = base_ast
    self.calculate_angle()
    self.calculate_distance_to_base()

  def __repr__(self):
    return(
      f'Asteroids {self.asteroids}\n'
      f'Base {self.base}'
    )

  def calculate_angle(self):
      for asteroid in self.asteroids:
          if asteroid.x == self.base.x and asteroid.y == self.base.y:
              continue
          asteroid.angle_with(self.base)

  def calculate_distance_to_base(self):
      for ast in self.asteroids:
          ast.distance = sqrt((self.base.x - ast.x) ** 2 + (self.base.y - ast.y) ** 2)

  def get_angle_set(self):
    angles = []
    for asteroid in self.asteroids:
        angles.append(asteroid.angle)
    return set(angles)
  
  def vaporise(self, amount, verbose):
    counter = 0 
    angle_set = self.get_angle_set()
    dict_angle = OrderedDict.fromkeys(sorted(angle_set))
    
    while(len(self.asteroids) > 0):
        for angle in dict_angle.keys():
          
          ast_vaporised = vaporise_next_asteroid(angle, self.asteroids, verbose)

          if verbose:
            print(f'Remove angle {angle}')
          
          counter += 1
          if counter == amount:
            return ast_vaporised

    return Asteroid(-1, -1)
          

def main():
  # N.B In solving this problem, I used matrix notation, which is the opposite of
  # how the problem is described ...
  # (0,0) (0,1) (0,2)
  # (1,0) (1,1) ...

  args = _get_args() 
  input_file_name = args.input
  verbose = args.verbose
  base = Asteroid(0,0)

  # part 1
  with open(input_file_name,'r') as file:
    mat = init_matrix(file)
    create_matrix(file, mat)
    
    print('Finding all asteroids')
    all_ast = np.nonzero(mat)
    asteroids_loc = []
    for i in range(len(all_ast[0])):
        asteroids_loc.append((all_ast[0][i], all_ast[1][i]))

    amount_asteroids = len(asteroids_loc)

    print(f'Looping over {amount_asteroids} and checking how many of all the other asteroids can be seen.')
    for asteroid in asteroids_loc:
        asteroids_seen = amount_asteroids - 1
        # Store directional vectors to all other asteroids in one vector
        directions_to_ast = []

        for other_ast in asteroids_loc:
            dir_vec = calculate_direction_vector(asteroid, other_ast)
            # check if current direction vector is colinear and has the same direction as any of the previous ones
            if is_colinear(dir_vec, directions_to_ast):
                asteroids_seen -= 1
        mat[asteroid[0], asteroid[1]] = asteroids_seen

    max_ast = np.where(mat == mat.max())
    # Assert that the matrix only has one maximum
    assert(len(max_ast[0]) == 1)
    print(max_ast)
    x_max = max_ast[0][0]
    y_max = max_ast[1][0]
    base = Asteroid(x_max, y_max)

    print(mat[x_max, y_max])
    print(f'The asteroid seeing most asteroids sees {mat.max()} other asteroids')
    print(f'and is located at line {x_max} and column {y_max}')

  #part 2
  with open(input_file_name,'r') as file:
    mat2 = init_matrix(file)
    create_matrix(file, mat2)
    
    print('Finding all asteroids')
    all_ast = np.nonzero(mat2)
    asteroids_loc = []
    asteroid_list = []
    for i in range(len(all_ast[0])):
        asteroids_loc.append((all_ast[0][i], all_ast[1][i]))
        ast = Asteroid(all_ast[0][i], all_ast[1][i])
        asteroid_list.append(ast)
    
    universe = Universe(asteroid_list, base)
    universe.asteroids.sort(key = lambda x: x.angle)
    
    # Remove base asteroids that end up at the first position
    universe.asteroids.pop(0)

    ast_to_rem = universe.vaporise(200, verbose)
    print(ast_to_rem)


if __name__ == '__main__':
  main()
