class MyClass:
    def __init__(self, atomic_list):
        self._atomic_list = atomic_list

    def apply(self, func):
        try:
            result = [
                func(item) for item in self._atomic_list
            ]  # applying func without modifying the saved list
            return result
        except Exception as e:  # error handling
            raise Exception(f"Error: {str(e)}")


my_list = [1, 2, 3, 4, 5]
p = MyClass(my_list)

cb_function = lambda x: x**3  # lambda function

try:
    processed_result = p.apply(cb_function)  # passing the cube function
    print(processed_result)
except Exception as ex:  # error handling
    print(f"Error: {str(ex)}")
