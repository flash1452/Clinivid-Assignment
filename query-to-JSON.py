



# Instructions to Run the program
#
#
# Modify the Query string in the variable query_string to change inputs.
# Run command """"python query-to-JSON.py"""" to run the script. 
# Return Value is the corresponding JSON for the query string 
#
#


import re
import json
from collections import OrderedDict

# Node structure for every node in the tree for every user's info below
class Node:
	def __init__(self):
		self.name = ""
		self.children = []


#
# Tree implemented through a list to store the structure/keys for user info. 
# Same structure will be used for personal info as well as followers info.
#
# Return -
#	Tree structure containing keys, making mapping values from query-string to keys easier and sequential.
#
def initialize_info_tree():
	temp_root_node = Node()
	temp_root_node.name = "profile"

	temp_node = Node()
	temp_node.name = "id"
	temp_root_node.children.append(temp_node)

	temp_node = Node()
	temp_node.name = "name"
	t_node1 = Node()
	t_node1.name = "first"
	t_node2 = Node()
	t_node2.name = "middle"
	t_node3 = Node() 
	t_node3.name = "last"
	temp_node.children.append(t_node1)
	temp_node.children.append(t_node2)
	temp_node.children.append(t_node3)
	temp_root_node.children.append(temp_node)

	temp_node = Node()
	temp_node.name = "location"
	t_node1 = Node()
	t_node1.name = "name"
	t_node2 = Node()
	t_node2.name = "coords"
	t_node21 = Node()
	t_node21.name = "long"
	t_node22 = Node()
	t_node22.name = "lat"
	t_node2.children.append(t_node21)
	t_node2.children.append(t_node22)
	temp_node.children.append(t_node1)
	temp_node.children.append(t_node2)
	temp_root_node.children.append(temp_node)

	temp_node = Node()
	temp_node.name = "imageId"
	temp_root_node.children.append(temp_node)

	return temp_root_node


#
# Function to validate balanced opening and closing bracket in the query string
# Args - 
#	expression     string    sub-queries from the query-string
#
# Return -
#	bool    whether query string is balanced or not. 
#
def validate_info_format(expression):
    opening = tuple('<')
    closing = tuple('>')
    mapping = dict(zip(opening, closing))
    queue = []

    for letter in expression:
        if letter in opening:
            queue.append(mapping[letter])
        elif letter in closing:
            if not queue or letter != queue.pop():
                return False
    return not queue


#
# Recursive function to  traverse through a user info tree and fill the keys with values
#
# Args -
#	personal_info_tree   	Node 	Tree structure for the user info returned from initialize_info_tree()
#	values 					List[]	List of values from query string enclosed in <> to be filled in the tree.
#
# Return -
#	personal_info_json		Dict 	Dictionary conatining the data for a user
#   
def traverse_query_string(personal_info_tree, values):
	personal_info_json = {}
	for node in personal_info_tree:
		if len(node.children) == 0:
			if len(values) > 0:
				personal_info_json[node.name] = values[0]
				values.pop(0)
		else:
			personal_info_json[node.name] = traverse_query_string(node.children, values)
	return personal_info_json


query_string    		= "profile|73241234|<Niharika><><Khan>|<Mumbai><<72.872075><19.075606>>|73241234.jpg**followers|54543343|<Amitabh><><>|<Dehradun><<><>>|54543343.jpg@@|22112211|<Piyush><><>||"
# Divide personal info and followers info
query_array     		= query_string.split('**')
# Extract query string related to the user
personal_info   		= query_array[0]
# Split personal info to get corresponding values to ID, Name, location and other values
split_personal_info 	= personal_info.split('|')
# All followers info extracted from query string into one
followers_agg_info  	= query_array[1]
# Get each followers info
split_followers_info	= followers_agg_info.split('@@')
flag					= 0
# Array to store all followers data Tree
followers_array 		= []
# check for brackets balance
for info in split_personal_info:
	if not validate_info_format(info):
		flag = 1
		break

if flag == 0:
	personal_info_tree  = Node()
	# Make the user info Tree.
	personal_info_tree  = initialize_info_tree()
	# Regular expression to extract the text between <> brackets.
	personal_info_data	= re.findall(r'<([^<>]*)>', personal_info)
	# Add Id at start and ImageId at end(since these two values not enclosed in <>) of the data array formed above
	personal_info_data.insert(0, split_personal_info[1])
	personal_info_data.append(split_personal_info[-1])
	# Parse the tree for keys and take corresponding values from personal_info_data and form a JSON object.
 	personal_info_obj 	= traverse_query_string(personal_info_tree.children, personal_info_data)

if flag == 1:
	print "Error in input string due to unbalanced parantheses."


# Decoding the followers part in the query-string and mapping it to the keys in the Tree.
if flag == 0:
	for each_follower_info in split_followers_info:
		each_follower_info_tree 	= Node()
		# Initialize tree for each follower
		each_follower_info_tree 	= initialize_info_tree()
		# Get data for each follower from query string
		split_each_follower_info 	= each_follower_info.split('|')
		flag 						= 0
		# check for brackets balance
		for info in split_each_follower_info:
			if not validate_info_format(info):
				flag = 1
				break
		if flag == 0:
			# Regular expression to extract the text between <> brackets.
			each_follower_info_data	= re.findall(r'<([^<>]*)>', each_follower_info)
			# Add Id at start and ImageId at end(since these two values not enclosed in <>) of the data array formed above
			each_follower_info_data.insert(0, split_each_follower_info[1])
			each_follower_info_data.append(split_each_follower_info[-1])
			# Parse the tree for keys and take corresponding values from personal_info_data and form a JSON object.
			each_follower_info_obj 	= traverse_query_string(each_follower_info_tree.children, each_follower_info_data)
			# Add each follower JSON object to follower array
			followers_array.append(each_follower_info_obj)
		if flag == 1:
			break
if flag == 1:
	print "Error in input string due to unbalanced parantheses."

# Add followers array to the personal info JSON.
personal_info_obj["followers"] = followers_array
print personal_info_obj