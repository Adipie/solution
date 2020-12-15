class Person(object):

    def __init__(self):
        super(Person, self).__init__()
        self.age = 1


class MagicList(list):

    def __init__(self, cls_type=None):
        super(MagicList, self).__init__()
        self.cls_type = cls_type

    def __getitem__(self, item):
        try:
            return super(MagicList, self).__getitem__(item)
        except IndexError:
            if self.cls_type:
                self.__setitem__(item, self.cls_type())
            else:
                self.__setitem__(item, None)
            return super(MagicList, self).__getitem__(item)

    def __setitem__(self, key, value):
        try:
            super(MagicList, self).__setitem__(key, value)
        except IndexError:
            if self.__len__() == key:
                self.append(value)
            else:
                raise IndexError


if __name__ == "__main__":
    # run without class type
    print("Magic list without class type")
    magic_list1 = MagicList()
    magic_list1[0] = 5
    print(magic_list1)

    # run with class type
    print("Magic list with class type")
    magic_list2 = MagicList(cls_type=Person)
    magic_list2[0].age = 5
    print(magic_list2)

    # run with class type, index order not kept
    print("Magic list with class type, index order not kept")
    magic_list3 = MagicList(cls_type=Person)
    try:
        magic_list3[1].age = 5
    except IndexError:
        print("caught expected index error")
