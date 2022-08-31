from config import ( copy,
                     secrets,
                     sym,
                     chunks_per_node,
                     number_of_nodes,
                     x,
)

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



# ==============
# Erasure Encode
# ==============

def erasure_encode(original_points, x_coordinates_extend) -> list:   
  polynomial = lagrange_interpolation(original_points)    
  
  # Make sure there are enough x_coordinates_extend to recover original file. 
  assert len(x_coordinates_extend) >= len(original_points)
  
  extended_points = extrapolate_points(polynomial, x_coordinates_extend)
  return extended_points



# ==============
# Lagrange Logic
# ==============

# Creates set of cubic polynomials that represent each file chunk, then adds all polynomials together,
# making a polynomial that uniquely represents the points given
def lagrange_interpolation(points):
  polynomials = []
  final_form_polynomials = [] 
  for i in range(len(points)):
    polynomials.append(one_and_zeros_polynomial(points[i][0], points))  
    final_form_polynomials.append(points[i][1]*expand_expression(polynomials[i][0])/operate_on_list(polynomials[i][1], multiply))
  final_polynomial = operate_on_list(final_form_polynomials, add)
  return final_polynomial 

# Creates a cubic polynomial whose valie is 1 at the x in question and 0 at all other x's
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
  def __init__(self):
    self.file_chunks = []

  def add_chunk(self, chunk):
    self.file_chunks.append(chunk)

def create_nodes() -> list[Node]:
  nodes = [] 
  for i in range(number_of_nodes):
    nodes.append(Node())  
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