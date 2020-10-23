import json
from typing import List
from collections import Counter


class Hardware:
    def __init__(self, id, ssd, ram, cost):
        self._id: int = id
        self.ssd: int = ssd
        self.ram: int = ram
        self.cost: int = cost


class Cost:
    def __init__(self, total, iva):
        self._total = total
        self.iva = iva

    @property
    def total(self):
        return self._total

    @total.setter
    def total(self, total):
        self._total = total


class Desglose:
    def __init__(self, id, ivi, ivo, ovo, uvu):
        self._id = id
        self.ivi = ivi
        self.ivo = ivo
        self._ovo = ovo
        self._uvu = uvu


class Laptop:
    def __init__(self, id, brand=None, processor=None, hardwares: List = None):
        self._id = id
        self._brand = brand
        self.processor = processor
        self.hardware = hardwares

    @property
    def brand(self):
        return self._brand
    # el brand sense el setter també el pille

    @property
    def processor(self):
        return self._processor

    @processor.setter
    def processor(self, processor):
        self._processor = processor


class JsonUtils:

    def to_dict(self, obj):
        """ Recursive class to get dictionaries from class or nested classes"""
        if not hasattr(obj, "__dict__"):
            return obj
        properties = self.check_getters_setters(obj)

        result = {}

        for key, val in obj.__dict__.items():
            if key in properties:
                # Aqui entre quan es una property
                key = key[1:]

                #todo: do recursive
            # Checking _id_mongo and elastic
            if key.startswith("_") and key is not "_id":
                continue

            element = []
            if isinstance(val, list):
                for item in val:
                    element.append(self.to_dict(item))
            else:
                element = self.to_dict(val)

            result[key] = element

        return result

    def check_getters_setters(self, obj):
        attr_list = list()

        for attr in dir(obj):
            # print("obj.%s = %r" % (attr, getattr(obj, attr)))
            if attr.startswith("_"):
                attr_list.append(attr)
            else:
                attr_list.append('_'+attr)

        d = Counter(attr_list)
        res = [k for k, v in d.items() if v > 1]
        return res


if __name__ == '__main__':
    # create object
    hardwares = list()
    costs = list()
    desglose = list()

    json_class = JsonUtils()

    desglose.append(Desglose(id=1,
                             ivi=20,
                             ivo=10,
                             ovo=5,
                             uvu=10))

    costs.append(Cost(total=1000,
                      iva=200))
    costs.append(Cost(total=2000,
                      iva=150))
    costs.append(Cost(total=1500,
                      iva=desglose))

    hardwares.append(Hardware(id=1,
                              ssd=256,
                              ram=16,
                              cost=costs))
    hardwares.append(Hardware(id=2,
                              ssd=512,
                              ram=32,
                              cost=costs))

    laptop = Laptop(id=1,
                    brand="Acer",
                    processor="Intel Core i7",
                    hardwares=hardwares)

    # laptop.brand = "Acer"

    dictionary = json_class.to_dict(obj=laptop)


    # write dict to json
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(dictionary, f, ensure_ascii=False, indent=4)
