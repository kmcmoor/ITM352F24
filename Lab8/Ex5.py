#Debugging exercise # 5
def fibonacci(list):
    Fibo = 0  
    for val in list:
        Fibo += val
    return Fibo

my_list = [1, 2, 3, 4, 5]
print(fibonacci(my_list))