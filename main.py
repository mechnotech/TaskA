INPUT = '''2
sandwich 7 3
butter 10 g
toasted_bread 2 cnt
sausage 30 g
omelet 9 4
egg 4 cnt
milk 120 ml
salt 1 g
sausage 50 g
7
egg 61 1 tens
milk 58 1 l
sausage 100 480 g
butter 120 180 g
cream 100 350 g
salt 14 1000 g
toasted_bread 40 20 cnt
8
egg 1 cnt 13 12 1 16.4
milk 1 l 3 4.5 4.7 60
chocolate 90 g 6.8 36.3 47.1 546
salt 1 kg 0 0 0 0
strawberry 100 g 0.4 0.1 7 35
sausage 100 g 10 18 1.5 210
toasted_bread 5 cnt 7.3 1.6 52.3 248
butter 100 g 0.8 72.5 1.3 661'''

INPUT = INPUT.split('\n')
pos = []
for i in INPUT:
    if 1 <= len(i) < 4:
        pos.append(INPUT.index(i))

Recipt_List = INPUT[1:pos[1]]
Price_List = INPUT[pos[1] + 1:pos[2]]
Calories_List = INPUT[pos[2] + 1:]

Dish_List = []
for i in Recipt_List:
    pos = i.split(' ')
    try:
        e = int(pos[2])
        s = Recipt_List.index(i)
        dish = pos[0], pos[1], Recipt_List[s + 1: s + e + 1]
        Dish_List.append(dish)
    except ValueError:
        pass


class CatalogNutr:
    def __init__(self):
        self.records = []

    def add_record(self, nutr):
        self.records.append(nutr)

    def show_plc(self, nutr, quant):  # вернуть расчет БЖУ в пересчете на число единиц (граммов, мл, шт)
        for i in self.records:
            if nutr in i.name:
                return i.proteins * quant, i.lipids * quant, i.carbs * quant, i.callories * quant


class PriceCatalog:
    def __init__(self):
        self.records = []

    def add_record(self, prod):
        self.records.append(prod)

    def show_price(self, prod):
        pass


class Nutrient:
    def __init__(self, string):
        string = string.split(' ')
        self.name = string[0]
        self.quantitiy = float(string[1])
        self.name_quant = string[2]
        delimiter = 1
        if self.name_quant == 'g' or self.name_quant == 'ml' or self.name_quant == 'cnt':
            delimiter = self.quantitiy
        if self.name_quant == 'kg':
            delimiter = 1000
            self.name_quant = 'g'
        if self.name_quant == 'l':
            delimiter = 1000
            self.name_quant = 'ml'
        if self.name_quant == 'tens':
            delimiter = 10
            self.name_quant = 'cnt'
        self.proteins = round((float(string[3]) / delimiter), 5)
        self.lipids = round((float(string[4]) / delimiter), 5)
        self.carbs = round((float(string[5]) / delimiter), 5)
        self.callories = round((float(string[6]) / delimiter), 5)


def Show_Quantity(product_dict):
    sum_price = 0
    for k, v in product_dict.items():
        for j in Price_List:
            row = j.split(' ')
            if k in row[0]:
                price = int(row[1])
                quant = int(row[2])
                name_quant = row[3]
                if name_quant == 'kg' or name_quant == 'l':
                    quant = quant * 1000
                if name_quant == 'tens':
                    quant = quant * 10
                ost = int(v / quant) + 1
                sum_price += price * ost
                product_dict[k] = ost
    return product_dict, sum_price


Calor_Obj = CatalogNutr()
for i in Calories_List:  # Заполнить справочник БЖУ и К
    Calor_Obj.add_record(nutr=Nutrient(string=i))

# Вывод блюд и их БЖК и К, создаем словарь с числом единиц каждого продукта
product_dict = {}
callories_otput = []
for i in Dish_List:
    list_ingr = i[2]
    num_person = int(i[1])
    p = l = c = cl = 0

    for j in list_ingr:
        ingr = j.split(' ')
        plc = Calor_Obj.show_plc(nutr=ingr[0], quant=int(ingr[1]))
        if ingr[0] in product_dict.keys():

            old_v = product_dict[ingr[0]]
            key = ingr[0]
            product_dict.update({key: old_v + num_person * int(ingr[1])})
        else:
            product_dict[ingr[0]] = num_person * int(ingr[1])
        p += plc[0]
        l += plc[1]
        c += plc[2]
        cl += plc[3]
    callories_otput.append((i[0], p, l, c, cl))

new_dict, sum_prce = Show_Quantity(product_dict)
print(sum_prce)
for k, v in product_dict.items():
    print(k, v)
for i in callories_otput:
    print(' '.join(map(str, i)))
