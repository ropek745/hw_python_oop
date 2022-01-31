class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self, training_type: str, duration: int,
                distance: float, speed: float, calories) -> None:

        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self):
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000

    def __init__(self, action: int, duration: int, weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

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
        message = InfoMessage(self.__class__.__name__, self.duration,
                              self.get_distance(),
                              self.get_mean_speed(),
                              self.get_spent_calories())
        return message

class Running(Training):
    """Тренировка: бег."""
    coe_cal_1= 18
    coe_cal_2 = 20
    def get_spent_calories(self):
        mean_speed = super().get_mean_speed()
        return (
            (self.coe_cal_1 * mean_speed - self.coe_cal_2)
             * self.weight / self.M_IN_KM * self.duration * 60
             )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    coef_cal_1 = 0.035
    coef_cal_2 = 0.029
    def __init__(self, 
                 action: int, 
                 duration: float, 
                 weight: float, 
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self):
        mean_speed = super().get_mean_speed()
        return (self.coef_cal_1 * self.weight + (mean_speed**2 // self.height)
         * self.coef_cal_2 * self.weight) * self.duration * 60



class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    def __init__(self, action: int,
                duration: float,
                weight: float,
                length_pool: float,
                count_pool: float) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self):
        return self.length_pool * self.count_pool / self.M_IN_KM / self.duration

    def get_spent_calories(self):
        return ((self.get_mean_speed() + 1.1) * 2 * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    if workout_type == 'SWM':
        count_rowing = data[0]
        duration = data[1]
        weight = data[2]
        pool_length = data[3]
        count_pool = data[4]
        swim = Swimming(count_rowing, duration ,
                        weight, pool_length, count_pool)
        return swim
    elif workout_type == 'RUN':
        count_step = data[0]
        duration_training = data[1]
        weight_user = data[2]
        run = Running(count_step, duration_training, weight_user)
        return run
    elif workout_type == 'WLK':
        count_step = data[0]
        duration_training = data[1]
        weight_user = data[2]
        heigth_user = data[3]
        walk = SportsWalking(count_step, duration_training,
                             weight_user, heigth_user)
        return walk


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


def run():
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)


if __name__ == '__main__':
    run()
