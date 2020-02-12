import numpy as np

def input_to_list(number):
  number_s = str(number)
  digit_list = []
  for elt in number_s:
    digit_list.append(int(elt))
  return digit_list

def count_nb(layer, nb):
  cnt = 0
  for pix in layer:
    if pix == nb:
      cnt += 1
  return cnt

def separate_to_layers(pixels, nb_pixels_in_layer):
  count = 0
  layers = []
  while(count < len(pixels)):
    cur_layer = []
    for i in range(0, nb_pixels_in_layer):
      pixel = pixels[count]
      cur_layer.append(pixels[count])
      count += 1
    layers.append(cur_layer)
  return layers

def main():
  with open('input.txt') as file:
    inp_string = file.read().strip()
    pixels = input_to_list(inp_string) 
    width = 25
    height = 6
    
    amount_layers = len(pixels) / (width * height)
    amount_pixels_in_layer = width * height
    print(f'Amount of layers: {amount_layers}')
    
    layers = separate_to_layers(pixels, amount_pixels_in_layer)

    # part 1
    layer_fewest_zeros = 0
    smallest_amount_zeros = amount_pixels_in_layer 
    for ix,layer in enumerate(layers):
      assert(len(layer) == width * height)
      amount_zeros = count_nb(layer,0)
      if amount_zeros < smallest_amount_zeros:
        smallest_amount_zeros = amount_zeros
        layer_fewest_zeros = ix

    amount1s = count_nb(layers[layer_fewest_zeros], 1)
    amount2s = count_nb(layers[layer_fewest_zeros], 2)
    print(f'Result part1 : {amount1s * amount2s}')

    # part 2
    image = np.empty((height, width,))
    image[:] = -1
    for layer in layers:
      for ix, pixel in enumerate(layer):
        x = int(ix / width)
        y = ix % width
        if image[x][y] != -1:
          continue
        if pixel == 2:
          continue
        if pixel == 1:
          image[x][y] = 1
        if pixel == 0:
          image[x][y] = 0
    print(image)

main()
