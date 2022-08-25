from helper import ( extrapolate_points,
                     lagrange_interpolation,
)

file = "1321"
file_chunks = [int(c) for c in file]
x_coordinates_for_original_file = [1,2,3,4]  
x_coordinates_for_duplication = [5,6,7,8]
original_points = list(zip(x_coordinates_for_original_file, file_chunks))

def erasure_encode(points, x_coordinates_duplicate):   
  polynomial = lagrange_interpolation(points)    
  extended_points = extrapolate_points(polynomial, x_coordinates_duplicate)
  return extended_points

# Proof of concept
extended_points = erasure_encode(original_points, x_coordinates_for_duplication)
original_points_derived = erasure_encode(extended_points, x_coordinates_for_original_file)
assert original_points_derived == original_points
print("Tah dahhh")