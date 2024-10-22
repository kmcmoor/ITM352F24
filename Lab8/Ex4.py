#Debugging exercise # 4
def get_element(list, index):
    return list[index]


my_list = [1, 2, 3, 4, 5]
print(get_element(my_list, 2))  
print(get_element(my_list, 4)) # Lists in Python are zero indexed, so my_list only goes from 0-4
