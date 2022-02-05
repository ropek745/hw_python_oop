from dataclasses import dataclass, fields
from typing import Sequence


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    PHRASE = (
        'Тип тренировки: {training_type}; '
        'Длительность: {duration:.3f} ч.; '
        'Дистанция: {distance:.3f} км; '
        'Ср. скорость: {speed:.3f} км/ч; '
        'Потрачено ккал: {calories:.3f}.'
    )
    
    def get_message(self) -> str:
        data_1 = self.training_type
        data_2 = self.duration
        data_3 = self.distance
        data_4 = self.speed
        data_5 = self.calories
        return self.PHRASE.format(
            training_type=data_1,
            duration=data_2,
            distance=data_3,
            speed=data_4,
            calories=data_5
        )


@dataclass
class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    M_IN_KM = 1000

    action: int
    duration: float
    weight: float

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        message = InfoMessage(
            self.__class__.__name__, 
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
            )
        return message

@dataclass
class Running(Training):
    """Тренировка: бег."""

    SPEED_MULTIPLIER_1 = 18
    SPEED_MULTIPLIER_2 = 20
    MINUTES = 60

    def get_spent_calories(self):
        speed = self.get_mean_speed()
        return ((self.SPEED_MULTIPLIER_1 * speed
                - self.SPEED_MULTIPLIER_2)
                * self.weight / self.M_IN_KM 
                * self.duration * self.MINUTES)

@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    SPEED_MULTIPLIER_1 = 0.035
    SPEED_MULTIPLIER_2 = 0.029
    MINUTES = 60

    action: int
    duration: float
    weight: float
    height: float

    def get_spent_calories(self):
        speed = self.get_mean_speed()
        return ((self.SPEED_MULTIPLIER_1 * self.weight
               + (speed**2 // self.height)
               * self.SPEED_MULTIPLIER_2 * self.weight)
               * self.duration * self.MINUTES)

@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    CALORIES_MULTIPLIER = 2
    CALORIES_SUMMATION = 1.1

    action: int
    duration: float
    weight: float
    length_pool: float
    count_pool: float

    def get_mean_speed(self):
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self):
        return ((self.get_mean_speed() + self.CALORIES_SUMMATION)
                * self.CALORIES_MULTIPLIER * self.weight)


def read_package(workout_type: str, data: Sequence) -> Training:
    """Прочитать данные полученные от датчиков."""

    workout_info = {
        'SWM': [Swimming, len(fields(Swimming))],
        'RUN': [Running, len(fields(Running))],
        'WLK': [SportsWalking, len(fields(SportsWalking))]
}
    for part in workout_info.values():
        if workout_type not in workout_info:
            raise KeyError('Тренировки нет в списке.')
        if workout_info[workout_type][1] != len(data):
            raise ValueError('Не соответствие набора элементов.')
        return workout_info[workout_type][0](*data)

def main(training: Training) -> None:
    """Главная функция."""
    print(training.show_training_info().get_message())

if __name__ == '__main__':
    packages = [      
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        main(read_package(workout_type, data))