import random

class Car:
    def __init__(self, trip_distance, model, color):
        self.fuel = random.randrange(0, 9)
        self.trip_distance = trip_distance
        self.model = model
        self.color = color


    def move(self, distance):
        if self.fuel - distance < 0:
            self.fuel += random.randrange(0, 9) # дозаправка та пропуск ходу, якщо недостатьно палива для руху на дистанцію
        else:
            self.fuel -= distance
            self.trip_distance += distance

cars = []
models = ["toyota", "bmw", "audi"]
colors = ["red", "white", "black"]
end_race = False
error = False
desired_dist = int(input("Відстань до фінішу(повинна бути більше нуля):"))

for number in range(1, 4):
    car_object = Car(trip_distance= 0, model= models[number - 1], color= colors[number - 1])
    cars.append(car_object)

if 0 >= desired_dist:
    print("error: Не вірно встановленно відстань до фінішу")
    error = True

while True:
    if error:
        break
    if end_race:
        break
    for car in cars:
        random_distance = random.randrange(0, 9)
        car.move(random_distance)

        if car.trip_distance >= desired_dist:
            print(f"Переможець цього заїзду: {car.model}, дистанцію яку було подоланно: {car.trip_distance}\n")
            end_race = True
            break
if not error:
    print("Статистика:")
    for car in cars:
        print(f"Автомобіль: {car.model}, подоланно дистанцію: {car.trip_distance}, залишилось палива: {car.fuel}")
