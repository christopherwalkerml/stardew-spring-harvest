season_duration = 28
globalist = {}

class Plant:
    def __init__(self, age, cost, sellprice, amount):
        self.age = age
        self.cost = cost
        self.amount = amount
        self.sellprice = sellprice
    def ageTick(self):
        self.age -= 1
        return self.age <= 0
    def getSellprice(self):
        return self.sellprice
    def setAge(self, age):
        self.age = age
    def getAmt(self):
        return self.amount
    def getCost(self):
        return self.cost
    def sell(self):
        return self.sellprice * self.amount
    def __repr__(self):
        return str({'age': self.age, 'amt': self.amount})
    def clone(self):
        return Plant(self.age, self.cost, self.sellprice, self.amount)

class Potato(Plant):
    age = 6
    cost = 50
    sellprice = 100
    
    def __init__(self, amt):
        self.amount = amt
        Plant(self.age, self.cost, self.sellprice, amt)

class Cauliflower(Plant):
    age = 12
    cost = 80
    sellprice = 175
    
    def __init__(self, amt):
        self.amount = amt
        Plant(self.age, self.cost, self.sellprice, amt)

class Parsnip(Plant):
    age = 4
    cost = 10
    sellprice = 35
    
    def __init__(self, amt):
        self.amount = amt
        Plant(self.age, self.cost, self.sellprice, amt)

class Strawberry(Plant):
    age = 8
    cost = 100
    sellprice = 122.4

    def __init__(self, amt):
        self.amount = amt
        Plant(self.age, self.cost, self.sellprice, amt)

def plant_crops(day, money, plants, history, networth):
    newplants = []
    hist = [h for h in history]
    net = networth[-1]
    nw = [n for n in networth]

    # check if plants can be sold, and if so, sell them
    for p in plants:
        if p.clone().ageTick():
            hist.append('day ' + str(day) + ' : sell ' + str(p.getAmt()) + ' ' + str(p.getSellprice()))
            money += p.sell()
            net += p.sell() - (p.cost * p.getAmt())
            if p.getSellprice() == Strawberry.sellprice and (day <= season_duration - 4):
                new_plant = p.clone()
                p.setAge(4)
                newplants.append(p.clone())
                net += (p.cost * p.getAmt())
        else:
            new_plant = p.clone()
            new_plant.ageTick()
            newplants.append(new_plant)

    # if spring is done, end traversal
    if day == season_duration:
        globalist[money] = [hist, nw + [net]]
        return

    if (day < 13):
        plant_crops(day + 1, money, newplants, hist, nw + [net])

    # plants can't be bought on a Wednesday or if they cant fully grow
    if (day + Potato.age <= season_duration) and (day % 3 != 0) and (money >= Potato.cost):
        amt = money // Potato.cost
        h = [hi for hi in hist]
        h.append('day ' + str(day) + ' : buy ' + str(amt) + ' potato')
        plant_crops(day + 1, money % Potato.cost, newplants + [Potato(amt)], h, nw + [net])
    else:
        plant_crops(day + 1, money, newplants, hist, nw + [net])

    if (day + Cauliflower.age <= season_duration) and (day % 3 != 0) and (money >= Cauliflower.cost):
        amt = money // Cauliflower.cost
        h = [hi for hi in hist]
        h.append('day ' + str(day) + ' : ' + str(amt) + ' cauli')
        plant_crops(day + 1, money % Cauliflower.cost, newplants + [Cauliflower(amt)], h, nw + [net])

    if (day == 13) and (money > Strawberry.cost):
        amt = money // Strawberry.cost
        h = [hi for hi in hist]
        h.append('day ' + str(day) + ' : ' + str(amt) + ' strawb')
        plant_crops(day + 1, money % Strawberry.cost, newplants + [Strawberry(amt)], h, nw + [net])
        

if __name__ == "__main__":
    plant_crops(1, 500, [Parsnip(15)], [], [650])
    plant_crops(1, 650, [], [], [650])

    with open('out.txt', 'w+') as f:
        f.write(str(dict(sorted(globalist.items()))))

