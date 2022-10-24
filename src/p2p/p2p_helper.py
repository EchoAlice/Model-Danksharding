from random import randint
from config import ( MAX_BIN_DIGITS, 
                     MAX_KEY,
)

# Which 'generate' function is better?
def generate_node_binary(x) -> str:
  node_binary = format(x, '0'+MAX_BIN_DIGITS+'b') 
  return node_binary 

# Move constants into the function. Constants shouldn't change
def generate_random_bitstring(max_int, digits) -> str:
  bitstring = format(randint(0, max_int), '0'+digits+'b')
  return bitstring

def populate_table(routing_table_obj) -> None:
  for i in range(MAX_KEY+1):
    peer_id = generate_node_binary(i)
    if peer_id != routing_table_obj.bin_id:  
      routing_table_obj.add_peer(peer_id)
  return