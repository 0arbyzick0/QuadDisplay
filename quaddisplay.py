from machine import Pin
import utime

class QuadDisplay:
    def __init__(self, segment_pins, digit_pins):
        """
        Инициализация дисплея.
        :param segment_pins: Список пинов для сегментов (a, b, c, d, e, f, g, dp).
        :param digit_pins: Список пинов для разрядов (Digit 1, Digit 2, Digit 3, Digit 4).
        """
        self.segments = [Pin(pin, Pin.OUT) for pin in segment_pins]
        self.digit_pins = [Pin(pin, Pin.OUT) for pin in digit_pins]
        
        # Паттерны для цифр 0-9, пустой клетки и точки
        self.digits = [
            [1, 1, 1, 1, 1, 0, 1, 0],  # 0
            [0, 1, 1, 0, 0, 0, 0, 0],  # 1
            [1, 1, 0, 1, 1, 1, 0, 0],  # 2
            [1, 1, 1, 1, 0, 1, 0, 0],  # 3
            [0, 1, 1, 0, 0, 1, 1, 0],  # 4
            [1, 0, 1, 1, 0, 1, 1, 0],  # 5
            [1, 0, 1, 1, 1, 1, 1, 0],  # 6
            [1, 1, 1, 0, 0, 0, 0, 0],  # 7
            [1, 1, 1, 1, 1, 1, 1, 0],  # 8
            [1, 1, 1, 1, 0, 1, 1, 0],  # 9
            [0, 0, 0, 0, 0, 0, 0, 0],  # Пустая клетка
            [0, 0, 0, 0, 0, 0, 0, 1]   # Точка
        ]

    def display_digit(self, num, position):
        """
        Отображает одну цифру или точку на указанном разряде.
        :param num: Цифра для отображения (0-9) или 10 для пустой клетки, 11 для точки.
        :param position: Позиция разряда (0-3).
        """
        for pin in self.digit_pins:
            pin.value(1)  # Выключаем все разряды
        self.digit_pins[position].value(0)  # Включаем нужный разряд
        
        for i in range(8):  # Устанавливаем сегменты
            self.segments[i].value(self.digits[num][i])

    def number(self, number, zeros=False, duration=1):
        """
        Отображает число на дисплее.
        :param number: Число для отображения (целое или дробное, например, 123 или 12.34).
        :param zeros: Если True, отображает ведущие нули.
        :param duration: Время отображения числа в секундах.
        """
        start_time = utime.time()  # Запоминаем время начала
        num_str = "{:04}".format(number) if isinstance(number, int) else "{:05}".format(number)
        while utime.time() - start_time < duration:  # Отображаем число в течение duration секунд
            for i in range(len(num_str)):
                char = num_str[i]
                if char == '.':
                    self.display_digit(11, i)  # Отображаем точку
                else:
                    digit = int(char)
                    if not zeros and digit == 0 and i < len(num_str) - 1:  # Пропускаем ведущие нули
                        self.display_digit(10, i)  # Пустая клетка
                    else:
                        self.display_digit(digit, i)
                utime.sleep_ms(5)  # Задержка для мультиплексирования
                self.clear()  # Очищаем дисплей перед следующим разрядом

    def clear(self):
        """Очищает дисплей (выключает все сегменты)."""
        for pin in self.digit_pins:
            pin.value(1)  # Выключаем все разряды
        for pin in self.segments:
            pin.value(0)  # Выключаем все сегменты
