import random
from cards import Card
from saving_invest_accounts import SavingAccount, InvestAccount


class Parent:

    def __init__(self, last_name, first_name, cards, children):
        self.last_name = last_name
        self.first_name = first_name
        self.cards = [Card(**card_data) for card_data in (cards or [])]
        self.num_cards = len(self.cards)
        self.children = [Child(**child_data) for child_data in (children or [])]
        self.save_accs = []
        self.invest_accs = []
        self.patterns = {}
        self.info = ''

    def __str__(self):
        s = ''
        s += f"My name is {self.first_name} {self.last_name} \n"
        s += f"I have {str(self.num_cards)} card(s) \n"
        s += f"I have {str(len(self.children))} children \n"
        s += self.info
        return s

    def buying(self):
        if self.num_cards != 0:
            card = self.cards[random.randint(0, self.num_cards) - 1]
            card.buying()
            self.info += card.buy_info

    def give_money(self):
        if self.num_cards != 0:
            card = self.cards[random.randint(0, self.num_cards) - 1]
            self.given_money = card.take_out()
            card.give_money()
            self.info += card.give_info

    def open_saving_account(self, acc_num, card_num=0, sum=0, per=5):
        if self.num_cards != 0:
            save_acc = SavingAccount(acc_num, sum, per)
            self.save_accs.append(save_acc)
            if sum != 0:
                card = self.cards[card_num - 1]
                card.open_save_acc(sum)
                save_acc.open_saving_account(sum, card.balance, card.number)
            else:
                save_acc.open_saving_account()
            self.info += save_acc.open_info

    def salary(self, sum):
        if self.num_cards != 0:
            card = self.cards[random.randint(0, self.num_cards) - 1]
            save_acc = self.save_accs[random.randint(0, len(self.save_accs)) - 1]
            save_acc.salary(sum)
            card.salary(sum, save_acc.per)
            self.salary_info = card.salary_info
            self.info += self.salary_info + save_acc.salary_info

    def deposit_save(self, num, card_num, sum):
        if self.num_cards != 0:
            save_acc = self.save_accs[num - 1]
            card = self.cards[card_num - 1]
            card.deposit_save(sum)
            save_acc.deposit_save(sum, card.number, card.balance )
            self.info += save_acc.deposit_save_info

    def withdraw_save(self, num, card_num, sum):
        if self.num_cards != 0:
            save_acc = self.save_accs[num - 1]
            card = self.cards[card_num - 1]
            card.withdraw_save(sum, save_acc.balance)
            save_acc.withdraw_save(sum, card.number, card.balance)
            self.info += save_acc.withdraw_info

    def transfer(self, data, card_num, sum):
        if self.num_cards != 0:
            card = self.cards[random.randint(0, self.num_cards) - 1]
            for i in range(len(data)):
                person = People(data[i]['last_name'], data[i]['first_name'], data[i]['cards'], data[i]['children'])
                for card_person in person.cards:
                    if card_person.number == card_num:
                        card_person.balance = card.transfer(card_person.balance, sum, card_num)
            self.info += card.transfer_info

    def open_invest_account(self, num):
        if self.num_cards != 0:
            invest_acc = InvestAccount(num)
            self.invest_accs.append(invest_acc)
            invest_acc.open_invest_account()
            self.info += invest_acc.open_info

    def deposit_invest(self, num, card_num, sum):
        if self.num_cards != 0:
            invest_acc = self.invest_accs[num - 1]
            card = self.cards[card_num - 1]
            card.deposit_invest(sum)
            invest_acc.deposit_invest(sum, card.number, card.balance)
            self.info += invest_acc.deposit_info

    def withdraw_invest(self, num, card_num, sum):
        if self.num_cards != 0:
            invest_acc = self.invest_accs[num - 1]
            card = self.cards[card_num - 1]
            card.withdraw_invest(sum, invest_acc.balance)
            invest_acc.withdraw_invest(sum, card.number, card.balance)
            self.info += invest_acc.withdraw_info

    def update_invest_account(self, num):
        if self.num_cards != 0:
            invest_acc = self.invest_accs[num - 1]
            invest_acc.update()
            self.info += invest_acc.update_info

    def create_pattern(self, card_num, name, sum):
        if self.num_cards != 0:
            card = self.cards[card_num - 1]
            self.patterns[name] = [sum, card.number, card.balance]
            card.create_pattern(name, sum)
            self.info += card.create_pattern_info

    def do_pattern(self, name):
        if self.num_cards != 0:
            pattern = self.patterns[name]
            for card in self.cards:
                if pattern[1] == card.number:
                    card.do_pattern(pattern[0], name)
                    self.info += card.do_pattern_info

class Child(Parent):

    def __init__(self, last_name, first_name, cards, age):
        super().__init__(last_name, first_name, cards,  children='')
        self.age = age

    def __str__(self):
        return super().__str__() + f"Also I am {self.age} \n" + self.give_info

    def buying(self):
        super().buying()

    def take_money(self, parent):
        if parent.num_cards != 0:
            self.taken_money = parent.given_money

    def put_in(self, parent):
        self.give_info = 'My parent didn\'t give me any money'
        if parent.num_cards != 0:
            if self.num_cards != 0:
                card = self.cards[random.randint(0,self.num_cards)-1]
                card.balance += self.taken_money
                card.balance = round(card.balance, 2)
            self.give_info = f"My parent gave me {self.taken_money}"

class People(Parent):
    def __init__(self, last_name, first_name, cards, children):
        super().__init__(last_name, first_name, cards, children)

#