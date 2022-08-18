def transpose(x):
  return -x

#  Should I use squared_number_of_equations or equations?
def create_equations(stub): 
  squared_number_equations= [[1^3, 1^2, 1^1, 0, -1],    
                             [2^3, 2^2, 2^1, 0, -3],
                             [3^3, 3^2, 3^1, 0, -2],
                             [4^3, 4^2, 4^1, 0, -1]]
  equations= [[1, 1, 1, 1, -1],
              [8, 4, 2, 1, -3],
              [27, 9, 3, 1, -2],
              [64, 16, 4, 1, -1]]             
  return equations

def extrapolate_points(formula):
  points = [] 
  return points