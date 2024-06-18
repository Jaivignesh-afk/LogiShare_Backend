class Example():
    name = "fafa"
    age = 10
    def __init__(self, name, age):
        self.name = name
        self.age = age

ex = Example("bhanu", 100)
ex1 = Example("bhaneu", 90)
print(ex.name, ex.age)
print(ex1.age, ex1.name)
