import math
import random
import secrets
import sympy as sym
x = sym.Symbol('x')

# Turn these variables into user generated, CLI inputs 
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
def convert_string_input():
  string_input = input('Enter string to encode: ')
  factor_of_extension = int(input('Enter factor (integer) to extend data by: '))

  file_chunks = [c for c in string_input.encode('ascii')]
  x_original = [x for x in range(1, len(file_chunks)+1)]       
  m = x_original[-1]
  n = m*factor_of_extension
  x_extension = [x for x in range(m+1, n+1)] 
  beginning_points = list(zip(x_original, file_chunks))
  
  return beginning_points, string_input, x_original, x_extension

def convert_node_input(all_points):
  number_of_nodes = int(input('Number of Nodes: '))
  chunks_per_node = int(input('Chunks per node: '))
  # probability_node_down = input('Probability node is down: ')  #  <---- Encorperate this one later
  
  min_number_of_nodes = math.ceil(len(all_points)/chunks_per_node)    
  if number_of_nodes >= min_number_of_nodes:
    return create_nodes(number_of_nodes), chunks_per_node
  else:
    print('Not enough storage available to reconstruct data...  Creating minimum number of nodes given chunks per node.') 
    return create_nodes(min_number_of_nodes), chunks_per_node 

# =============
# Erasure Logic
# =============
def erasure_code(original_points, x_coordinates_for_new_points) -> list:   
  polynomial = lagrange_interpolation(original_points)    
  
  # Make sure there are enough x_coordinates_extend to recover original file. 
  assert len(x_coordinates_for_new_points) >= len(original_points)
  
  new_points = extrapolate_points(polynomial, x_coordinates_for_new_points)
  return new_points

# ==============
# Lagrange Logic
# ==============
# Creates set of polynomials that represent each file chunk, then adds all polynomials together,
# making a polynomial that uniquely represents the points given
def lagrange_interpolation(points):
  polynomials = []
  final_form_polynomials = [] 
  for i in range(len(points)):
    polynomials.append(one_and_zeros_polynomial(points[i][0], points))  
    final_form_polynomials.append(points[i][1]*expand_expression(polynomials[i][0])/operate_on_list(polynomials[i][1], multiply))
  final_polynomial = operate_on_list(final_form_polynomials, add)
  return final_polynomial 

# Creates a polynomial whose value is 1 at the x in question and 0 at all other x's
def one_and_zeros_polynomial(x_in_question, points):
  basic_polynomial = []
  for i in range(2):
    half_poly = []
    for point in points:
      if x_in_question != point[0]:
        if i == 0:
          half_poly.append((x - point[0]))  
        if i == 1:
          half_poly.append((x_in_question - point[0]))
    basic_polynomial.append(half_poly) 
  return basic_polynomial

def extrapolate_points(polynomial, x_coordinates):
  extended_file_chunks = [] 
  for x_coordinate in x_coordinates: 
    y = polynomial.subs({x:x_coordinate})
    extended_file_chunks.append((x_coordinate,y))
  return extended_file_chunks

# ==========
# Node Logic 
# ==========
class Node:
  def __init__(self, index):
    self.index = index 
    self.file_chunks = []
    self.status = True

  def add_chunk(self, chunk):
    self.file_chunks.append(chunk)

  def pop_chunk(self, chunk_index):
    self.file_chunks.pop(chunk_index)

def create_nodes(number_of_nodes) -> list[Node]:
  nodes = [] 
  for i in range(number_of_nodes):
    nodes.append(Node(i))  
  return nodes 

def distribute_file_chunks(nodes, all_points, chunks_per_node) -> list[Node]:                    
  chunk_increment = 0
  for c in range(chunks_per_node):           
    for n in range(len(nodes)):
      i = chunk_increment % len(all_points) 
      nodes[n].add_chunk(all_points[i]) 
      chunk_increment += 1
  return nodes

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

  print("Encoded file chunks: "+str(points_for_reconstruction))
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