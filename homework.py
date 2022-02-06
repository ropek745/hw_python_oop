from dataclasses import dataclass, fields, asdict
from typing import Sequence


TRAINING_ERROR = 'Тренировки {workout_type} нет в программе!'
DATA_ERROR = (
    'Количество элементов {false_data}'
    'не предусмотрено для {sport}}! '
    'Для {sport} нужно '
    '{true_data} элементов!'
)


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
        return self.PHRASE.format(**asdict(self))


@dataclass
class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    M_IN_KM = 1000
    DURATION_MULTIPLIER = 60

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

    SPEED_MULTIPLIER = 18
    SUBTRACTED_FROM_SPEED = 20

    def get_spent_calories(self):
        speed = self.get_mean_speed()
        return (
            (self.SPEED_MULTIPLIER * speed
             - self.SUBTRACTED_FROM_SPEED) * self.weight
            / self.M_IN_KM * self.duration * self.DURATION_MULTIPLIER
        )


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    WEIGTH_MULTIPLIER_1 = 0.035
    WEIGTH_MULTIPLIER_2 = 0.029

    height: float

    def get_spent_calories(self):
        speed = self.get_mean_speed()
        return (
            (self.WEIGTH_MULTIPLIER_1 * self.weight
             + (speed ** 2 // self.height)
             * self.WEIGTH_MULTIPLIER_2 * self.weight)
            * self.duration * self.DURATION_MULTIPLIER
        )


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    SPEED_MULTIPLIER = 2
    SPEED_SUMMATION = 1.1

    length_pool: float
    count_pool: int

    def get_mean_speed(self):
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self):
        return ((self.get_mean_speed() + self.SPEED_SUMMATION)
                * self.SPEED_MULTIPLIER * self.weight)


WORKOUT_INFO = {
    'SWM': [Swimming, len(fields(Swimming))],
    'RUN': [Running, len(fields(Running))],
    'WLK': [SportsWalking, len(fields(SportsWalking))]
}


def read_package(workout_type: str, data: Sequence) -> Training:
    """Прочитать данные полученные от датчиков."""

    if workout_type not in WORKOUT_INFO:
        raise ValueError(TRAINING_ERROR.format(workout_type))
    if WORKOUT_INFO[workout_type][1] != len(data):
        raise ValueError(DATA_ERROR.format(
            false_data=len(data),
            sport=workout_type,
            true_data=WORKOUT_INFO[workout_type][1])
        )
    return WORKOUT_INFO[workout_type][0](*data)


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
