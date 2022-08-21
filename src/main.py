from helper import ( create_equations,
                     system_solve,
                     extrapolate_points,
)
# Questions for user:
#    How many chunks do you want to split the file into?
#    How many chunks need to be gathered in order to reconstruct the entire file?
#    How many extended chunks do you want to create?

file = "1321"
x_coordinates_for_original_file = [1,2,3,4]  
x_coordinates_for_duplication = [5,6,7,8]
split_increments = len(x_coordinates_for_original_file)     #  Get argument from user as to how many chunks to split the file into 

# Splits up file 
proto_file_chunks = [int(file[i:i+split_increments]) for i in range(0, len(file), split_increments)]
file_chunks = [1,3,2,1]


# Represent formulas as list of coefficients.  Set equation equal to zero
#                        [x_coordinate, y-intercept, y_coordinate]
# Example:  1*a + b - 13 = 0   --> [1,     1,     -13]   
#           2*a + b - 21 = 0   --> [2,     1,     -21]
#
#  We have the coefficients that represent the linear equations, now we need the point to evaluate it at         

def erasure_encode(file_chunks) -> int:   
  final_y = file_chunks[-1]
  final_equation = [] 
  archive_equations = [] 
  equations = create_equations(file_chunks)
  #  Why does this function not return my polynomial? 
  broken_polynomial = system_solve(equations, archive_equations, final_y) 
  polynomial = [0.5, -4.5, 12.0, -7.0] 
  extended_file_chunks = extrapolate_points(polynomial, x_coordinates_for_duplication)
  return polynomial, extended_file_chunks 