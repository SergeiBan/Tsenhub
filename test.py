class Person:
    def __init__(self, name) -> None:
        self.name = name

    def say(self, message):
        print(f'{self.name} says {message}')


class Doggo:
    def __init__(self, name) -> None:
        self.name = name

    def bark(self, message):
        print(f'bark bark {message} bark')


class Shout:
    def __init__(self, person) -> None:
        self.person = person

    def shout(self, message):
        self.person.say(message.upper())


keks = Doggo('keks')
keks.bark('henlo fren')

sergei = Person('sergei')
sergei.say('hi')

loud_sergei = Shout(sergei)
loud_sergei.shout('hi')


class DoggoAdapterToPerson:
    def __init__(self, doggo) -> None:
        self.doggo = doggo

    def say(self, message):
        self.doggo.bark(message)


keks_apapter = DoggoAdapterToPerson(keks)
loud_keks = Shout(keks_apapter)

loud_keks.shout('henlo fren')