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
        
        # Паттерны для цифр 0-9 и пустой клетки
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
            [0, 0, 0, 0, 0, 0, 0, 0]   # Пустая клетка
        ]

    def display_digit(self, num, position):
        """
        Отображает одну цифру на указанном разряде.
        :param num: Цифра для отображения (0-9).
        :param position: Позиция разряда (0-3).
        """
        for pin in self.digit_pins:
            pin.value(1)  # Выключаем все разряды
        self.digit_pins[position].value(0)  # Включаем нужный разряд
        
        for i in range(8):  # Устанавливаем сегменты
            self.segments[i].value(self.digits[num][i])

    def display_number(self, number, leading_zeros=False, duration=1):
        """
        Отображает 4-значное число на дисплее.
        :param number: Число для отображения (0-9999).
        :param leading_zeros: Если True, отображает ведущие нули.
        :param duration: Время отображения числа в секундах.
        """
        start_time = utime.time()  # Запоминаем время начала
        while utime.time() - start_time < duration:  # Отображаем число в течение duration секунд
            num_str = "{:04d}".format(number)
            for i in range(4):
                digit = int(num_str[i])
                if not leading_zeros and digit == 0 and i < 3:  # Пропускаем ведущие нули
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

# Пример использования
segment_pins = [15, 14, 13, 12, 11, 10, 9, 8]  # Пины для сегментов
digit_pins = [16, 17, 18, 19]  # Пины для разрядов

display = QuadDisplay(segment_pins, digit_pins)

# Бесконечный цикл для отображения чисел
while True:
    # Отображаем число 256 с ведущими нулями в течение 5 секунд
    display.display_number(256, leading_zeros=True, duration=5)
    
    # Отображаем число 257 без ведущих нулей в течение 5 секунд
    display.display_number(257, leading_zeros=False, duration=5)
