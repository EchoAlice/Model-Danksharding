from helper import ( extrapolate_points,
                     lagrange_interpolation,
)

#  Get argument from user as to how many chunks to split the file into

# Questions for user:
#    How many chunks do you want to split the file into?
#    How many chunks need to be gathered in order to reconstruct the entire file?
#    How many extended chunks do you want to create?

file = "1321"
file_chunks = [int(c) for c in file]
x_coordinates_for_original_file = [1,2,3,4]  
x_coordinates_for_duplication = [5,6,7,8]
points = list(zip(x_coordinates_for_original_file, file_chunks))

def erasure_encode(points):   
  polynomial = lagrange_interpolation(points)    
  extended_file_chunks = extrapolate_points(polynomial, x_coordinates_for_duplication)
  return extended_file_chunks

extended_file_chunks = erasure_encode(points)