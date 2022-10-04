import math
import numbers
import random
import secrets
import sympy as sym
from remerkleable.basic import uint64, byte
from remerkleable.complex import Container, Vector


x = sym.Symbol('x')

# e = mkModuloClass(11)
Bytes16 = Vector[byte, 16]                        # Test value for now
Bytes512 = Vector[byte, 512]
sample = byte                                     # A sample is actually a 512 byte chunk!

probability_node_is_down = 0.1

# ===============
# Basic Functions
# ===============
def add(a,b):
  return a+b 

def multiply(a,b):
  return a*b

def transpose(num):
  return -num

def expand_expression(list_of_expressions):
  expanded_expression = list_of_expressions[0] 
  for i in range(len(list_of_expressions)-1):
    expanded_expression = sym.expand(expanded_expression*list_of_expressions[i+1])
  return expanded_expression

def operate_on_list(list, operation):
  if len(list) == 1:
    return list[0]
  else:
    list[-2] = operation(list[-1],list[-2])
    list.pop(-1)
    return operate_on_list(list, operation)

# ===========
# Input Logic 
# ===========
#
#    Mock a blob
def convert_string_input(string_input):
  factor_of_extension = 2 
  file_chunks = [c for c in string_input.encode('ascii')]             #  At some point, have file chunks equivalent to 512 bytes each (mock shards) 
  x_original = [x for x in range(1, len(file_chunks)+1)]       
  m = x_original[-1]
  n = m*factor_of_extension
  x_extension = [x for x in range(m+1, n+1)] 
  beginning_points = list(zip(x_original, file_chunks))
  return beginning_points, x_original, x_extension

#     Mock a subnet
def convert_node_input(all_points):
  number_of_nodes = 1
  chunks_per_node = 1
  min_number_of_nodes = math.ceil(len(all_points)/chunks_per_node)    
  if number_of_nodes >= min_number_of_nodes:
    return create_storage_nodes(number_of_nodes), chunks_per_node
  else:
    return create_storage_nodes(min_number_of_nodes), chunks_per_node 


# ==========================
# Lagrange Logic (Vitalik's)
# ==========================
#
# We explicitely define xs and xs_to_derive outside of this function so
# we can use this function to extend data or reconstruct original data.
def reed_solomon_data(data, xs, xs_to_derive) -> list[sample]:                        
  # polynomial = lagrange_interp(data, xs)
  polynomial = lagrange_interpolation(data, xs)    
  derived_chunks = extrapolate_chunks_my_version(polynomial, xs_to_derive)
  return derived_chunks

# Modular division class
def mkModuloClass(n):
  if pow(2, n, n) != 2:
    raise Exception("n must be prime!")

  class Mod:
    val = 0

    def __init__(self, val):
      self.val = val.val if isinstance(
        self.val, self.__class__) else val

    def __add__(self, other):
      return self.__class__((self.val + other.val) % n)

    def __mul__(self, other):
      return self.__class__((self.val * other.val) % n)

    def __sub__(self, other):
      return self.__class__((self.val - other.val) % n)

    def __truediv__(self, other): 
      return self.__class__((self.val * other.val ** (n-2)) % n)

    def __int__(self):
      return self.val

    def __repr__(self):
      return repr(self.val)
  return Mod

def lagrange_interp(pieces, xs):
    arithmetic = pieces[0].__class__
    zero, one = arithmetic(0), arithmetic(1)
    # Generate master numerator polynomial
    root = [one]
    for i in range(len(xs)):
        root.insert(0, zero)
        for j in range(len(root)-1):
            root[j] = root[j] - root[j+1] * xs[i]
    # Generate per-value numerator polynomials by dividing the master
    # polynomial back by each x coordinate
    nums = []
    for i in range(len(xs)):
        output = []
        last = one
        for j in range(2, len(root)+1):
            output.insert(0, last)
            if j != len(root):
                last = root[-j] + last * xs[i]
        nums.append(output)
    # Generate denominators by evaluating numerator polys at their x
    denoms = []
    for i in range(len(xs)):
        denom = zero
        x_to_the_j = one
        for j in range(len(nums[i])):
            denom += x_to_the_j * nums[i][j]
            x_to_the_j *= xs[i]
        denoms.append(denom)
    # Generate output polynomial
    b = [zero for i in range(len(pieces))]
    for i in range(len(xs)):
        yslice = pieces[int(i)] / denoms[int(i)]
        for j in range(len(pieces)):
            b[j] += nums[i][j] * yslice
    return b

# USE THIS VERSION OF EXTRAPOLATE_CHUNKS() WITH LAGRANGE_INTERP()
#----------------------------------------------------------------
# def extrapolate_chunks(polynomial, xs):                             
#   extended_chunks=[]   
#   for x in xs:
#     sample = round(solve_x(x,polynomial)) 
#     # sample = solve_x(x,polynomial) 
#     extended_chunks.append(sample) 
#   return extended_chunks

def extrapolate_chunks_my_version(polynomial, xs):                             
  extended_file_chunks = [] 
  for x_coordinate in xs: 
    y = polynomial.subs({x:x_coordinate})
    extended_file_chunks.append(y)
  return extended_file_chunks

def solve_x(x, polynomial):
  # Sets up the type of math you're using (int or Mod) 
  arithmetic = x.__class__ 
  zero, one = arithmetic(0), arithmetic(1) 
  
  y = zero
  power_val = x
  for i in range(len(polynomial)):
    if i == 0:
      power_val = one 
    y += polynomial[i]*power_val 
    power_val *= x  
  return y

# =====================
# Lagrange Logic (Mine)
# =====================

def reed_solomon_points(data, xs, extended_xs) -> list:   
  polynomial = lagrange_interpolation(data, xs)    
  new_points = extrapolate_points(polynomial, extended_xs)             
  return new_points

# Creates set of polynomials that represent each file chunk, then adds all polynomials together,
# making a polynomial that uniquely represents the points given
def lagrange_interpolation(data, xs):

  polynomials = []
  final_polynomial = [] 
  for i in range(len(data)):
    polynomials.append(one_and_zeros_polynomial(xs[i], xs))  
    final_polynomial.append(data[i]*expand_expression(polynomials[i][0])/operate_on_list(polynomials[i][1], multiply))

  final_polynomial = operate_on_list(final_polynomial, add)
  
  # Create a polynomial with just the coefficients! 
  return final_polynomial 

# Creates a polynomial whose value is 1 at the x in question and 0 at all other x's
def one_and_zeros_polynomial(x_in_question, xs):
  basic_polynomial = []
  for i in range(2):
    half_poly = []
    for j in range(len(xs)):
      if x_in_question != xs[j]:
        if i == 0:
          half_poly.append((x - xs[j]))  
        if i == 1:
          half_poly.append((x_in_question - xs[j]))
    basic_polynomial.append(half_poly) 
  return basic_polynomial

def extrapolate_points(polynomial, x_coordinates):
  extended_file_chunks = [] 
  for x_coordinate in x_coordinates: 
    y = polynomial.subs({x:x_coordinate})
    # extended_file_chunks.append(y)
    extended_file_chunks.append((x_coordinate,y))
  return extended_file_chunks



# ===================
# STORAGE NODES (old)              
# ===================                Maybe recycle these to each store blob data

class StorageNode:
  def __init__(self, index):
    self.index = index 
    self.file_chunks = []
    self.status = True

  def add_chunk(self, chunk):
    self.file_chunks.append(chunk)

  def pop_chunk(self, chunk_index):
    self.file_chunks.pop(chunk_index)

def create_storage_nodes(number_of_nodes) -> list[StorageNode]:
  storage_nodes = [] 
  for i in range(number_of_nodes):
    storage_nodes.append(StorageNode(i))  
  return storage_nodes 

def distribute_file_chunks(storage_nodes, all_points, chunks_per_node) -> list[StorageNode]:                    
  chunk_increment = 0
  for c in range(chunks_per_node):           
    for n in range(len(storage_nodes)):
      i = chunk_increment % len(all_points) 
      storage_nodes[n].add_chunk(all_points[i]) 
      chunk_increment += 1
  return storage_nodes

def apply_probability(nodes, probability):
  for node in nodes: 
    rand = random.uniform(0,1)
    if rand <= probability:
      node.status = False 


# ====================
# Reconstruction Logic 
# ====================
def gather_chunks(full_nodes, x_coordinates_for_original_file):
  apply_probability(full_nodes, probability_node_is_down)
  points_for_reconstruction = [] 
  
  while len(points_for_reconstruction) < len(x_coordinates_for_original_file): 
    node_in_question = secrets.choice(full_nodes)
    if len(node_in_question.file_chunks) > 0 and node_in_question.status == True:
      random_chunk_index = secrets.randbelow(len(node_in_question.file_chunks))
      chunk = node_in_question.file_chunks[random_chunk_index]
      if redundancy_algorithm(chunk, points_for_reconstruction) == False:
        points_for_reconstruction.append(chunk)                  #  <---- Organize encoded_file_chunks in a more efficient way
        node_in_question.pop_chunk(random_chunk_index)        #  <---- This feels awkward

  return points_for_reconstruction

#  First organize placing chunks in list smallest x ---> largest x, then worry about creating a better function
#  I believe this linear search is better (than organizing list and then inserting) up to a certain point.  
#  What is that point???
def redundancy_algorithm(chunk_in_question, encoded_file_chunks) -> bool:
  if len(encoded_file_chunks) > 0: 
    for i in range(len(encoded_file_chunks)):
      if chunk_in_question == encoded_file_chunks[i]:  
        return True
  return False   

def points_to_string(points):
  file_list = [] 
  for point in points:
    file_list.append(point[1]) 
  file = bytes(file_list).decode() 
  return file


















# =============
# RANDOM VALUES
# =============
def random_chunks_and_xs(points):
  points_chosen = [] 
  number_of_chunks = int(len(points)/2)  
  for i in range(number_of_chunks):
    random_point = secrets.choice(points)
    points_chosen.append(random_point)
    points.remove(random_point) 
  return points_chosen