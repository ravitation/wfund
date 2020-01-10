#!/usr/bin/env python
# _*_ coding=utf-8 _*_
import random
import datetime
from utils.util import gen_random
from resources.material.division import Division
from resources.material.spell import WordDict
from resources.material.surname import Surname


class IdCard:
    month_day = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    wi = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2, 1]
    vi = ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2']

    def __init__(self):
        divi = self.gen_divi()
        birth = self.gen_birth()
        self.division = Division.all_name(divi)
        pre_no = str(divi) + str(birth) + str(gen_random(3))
        self.card_no = pre_no + str(self.gen_valid(pre_no))
        self.name = self.gen_name()
        pass

    @classmethod
    def gen_birth(cls):
        now_year = datetime.datetime.now().year
        year = random.randint(1910, now_year)
        month = random.randint(0, 11)
        day = random.randint(1, IdCard.month_day[month])
        month = month if len(str(month)) == 2 else '0' + str(month)
        day = day if len(str(day)) == 2 else '0' + str(day)
        return str(year) + str(month) + str(day)

    @classmethod
    def gen_divi(cls):
        return random.sample([x.value for x in Division.__iter__() if not str(x.value[0]).endswith('00')], 1)[0][0]

    @classmethod
    def gen_valid(cls, no):
        card = no[0:18]
        li = list(card)
        num = 0
        for it in range(len(li)):
            num += IdCard.wi[it] * int(li[it])
        return IdCard.vi[num % 11]

    @classmethod
    def gen_name(cls):
        pin = []
        name = []
        for i in range(random.randint(1, 2)):
            py = WordDict.random_py()
            for p in py:
                pin.append(p)
                name.append(random.sample(py[p], 1)[0])

        surname = cls.gen_surname()
        for i in surname:
            pin.insert(0, i)
            name.insert(0, surname[i])
        return {' '.join(pin): ''.join(name)}

    @classmethod
    def gen_surname(cls):
        pin = []
        name = []
        surname = Surname.random()
        json = WordDict.to_word_json()
        for i in range(len(surname)):
            pin.append(random.sample(json[surname[i]], 1)[0])
            name.append(surname[i])
        return {' '.join(pin): ''.join(name)}


if __name__ == '__main__':
    a = IdCard()
    print(a.name)
    print(a.card_no)
    print(a.division)

    # spell = {m: n for m, n in [k.value for k in WordDict.__members__.values()]}
