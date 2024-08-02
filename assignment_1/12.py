class MyClass:
    def __init__(self, atomic_list):
        self._atomic_list = atomic_list

    def apply(self, func):
        try:
            result = [func(item) for item in self._atomic_list]
            return result
        except Exception as e:
            raise Exception(f"Error processing the list: {str(e)}")


if __name__ == "__main__":
    my_list = [1, 2, 3, 4, 5]
    processor = MyClass(my_list)

    square_function = lambda x: x**3

    try:
        processed_result = processor.apply(square_function)
        print(processed_result)
    except Exception as ex:
        print(f"Error: {str(ex)}")
