# class Foo(object):
#     def __init__(self, name):
#         self.name = name
#
#     def func(self):
#         return f"{self.name}:属性方法"
#
#     @property
#     def pro(self):
#         return f"{self.name}:属性方法"
#
#
# if __name__ == '__main__':
#     foo_obj = Foo("alex")
#     # foo_obj.func()
#     print(foo_obj.pro)
class A(object):

    count = 0

    def __init__(self):
        self.name = "yoyo"
        self.age = 18

    def start(self):
        print("start1111111")

    def __getitem__(self, item):
        return object.__getattribute__(self, item)

a = A()
print(a.count)
print(a.name)
# 通过[key]语法调用属性
print(a['count'])
print(a['age'])
print(a['start'])
print(a['start']())
