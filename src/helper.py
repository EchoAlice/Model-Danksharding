import secrets
import sympy as sym
x = sym.Symbol('x')

# Turn these variables into user generated, CLI inputs 
number_of_nodes = 5
chunks_per_node = 2
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
# Make sure these things have conditions to protect us from weird things happening
def convert_input():
  string_input = input('Enter a string of numbers to encode: ')
  factor_of_extension = int(input('Enter factor (integer) to extend data by: '))

  file_chunks = [int(c) for c in string_input]
  x_original = [x for x in range(1, len(file_chunks)+1)]       
  m = x_original[-1]
  n = m*factor_of_extension
  x_extension = [x for x in range(m+1, n+1)] 
  beginning_points = list(zip(x_original, file_chunks))
  return beginning_points, string_input, x_original, x_extension

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

  def add_chunk(self, chunk):
    self.file_chunks.append(chunk)

  def pop_chunk(self, chunk_index):
    self.file_chunks.pop(chunk_index)


def create_nodes() -> list[Node]:
  nodes = [] 
  for i in range(number_of_nodes):
    nodes.append(Node(i))  
  return nodes 

# Distribute file chunks explicitely to insure there isn't too much redundancy
def distribute_file_chunks(nodes, n_file_chunks) -> list:                    
  chunk_increment = 0
  for c in range(chunks_per_node): 
    for n in range(number_of_nodes):
      i = chunk_increment % 8 
      nodes[n].add_chunk(n_file_chunks[i]) 
      chunk_increment += 1
  return nodes

def reconstruct_file(full_nodes, x_coordinates_for_original_file):
  encoded_file_chunks = [] 
  
  while len(encoded_file_chunks) < len(x_coordinates_for_original_file): 
    for node in full_nodes:
      print(node.file_chunks) 
    
    node_in_question = secrets.choice(full_nodes)
    if len(node_in_question.file_chunks) > 0:
      random_chunk_index = secrets.randbelow(len(node_in_question.file_chunks))
      chunk_in_question = node_in_question.file_chunks[random_chunk_index]
      if redundancy_algorithm(chunk_in_question, encoded_file_chunks) == False:
        encoded_file_chunks.append(chunk_in_question)
        node_in_question.pop_chunk(random_chunk_index)

  print("Encoded file chunks: "+str(encoded_file_chunks))
  original_points = erasure_code(encoded_file_chunks, x_coordinates_for_original_file)    
  original_file = points_to_string(original_points) 
  
  return original_file 

# Make this thing a lot cooler... Right now, the algorithm scales linearly.  No bueno 
def redundancy_algorithm(chunk_in_question, encoded_file_chunks) -> bool:
  if len(encoded_file_chunks) > 0: 
    for i in range(len(encoded_file_chunks)):
      if chunk_in_question == encoded_file_chunks[i]:  
        return True
  return False   

def points_to_string(points):
  file_list = [] 
  for point in points:
    file_list.append(str(point[1])) 
  file = ''.join(file_list)
  return file