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
        
        # Паттерны для символов (0-9, A-Z, пробел, минус, точка, звезда, подчеркивание)
        self.digits = [
            # Без точки
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
            
            # С точкой
            [1, 1, 1, 1, 1, 0, 1, 1],  # 0.
            [0, 1, 1, 0, 0, 0, 0, 1],  # 1.
            [1, 1, 0, 1, 1, 1, 0, 1],  # 2.
            [1, 1, 1, 1, 0, 1, 0, 1],  # 3.
            [0, 1, 1, 0, 0, 1, 1, 1],  # 4.
            [1, 0, 1, 1, 0, 1, 1, 1],  # 5.
            [1, 0, 1, 1, 1, 1, 1, 1],  # 6.
            [1, 1, 1, 0, 0, 0, 0, 1],  # 7.
            [1, 1, 1, 1, 1, 1, 1, 1],  # 8.
            [1, 1, 1, 1, 0, 1, 1, 1],  # 9.
            
            # Буквы A-Z
            [1, 1, 1, 0, 1, 1, 1, 0],  # A
            [0, 0, 1, 1, 1, 1, 1, 0],  # b
            [1, 0, 0, 1, 1, 0, 1, 0],  # C
            [0, 1, 1, 1, 1, 1, 0, 0],  # d
            [1, 0, 0, 1, 1, 1, 1, 0],  # E
            [1, 0, 0, 0, 1, 1, 1, 0],  # F
            [1, 0, 1, 1, 1, 0, 1, 0],  # G
            [0, 1, 1, 0, 1, 1, 1, 0],  # H
            [0, 0, 0, 0, 1, 0, 1, 0],  # I
            [0, 1, 1, 1, 0, 0, 0, 0],  # J
            [1, 0, 1, 0, 1, 1, 1, 0],  # K
            [0, 0, 0, 1, 1, 0, 1, 0],  # L
            [0, 0, 0, 0, 0, 0, 0, 0],  # M (не отображается)
            [1, 1, 1, 0, 1, 0, 1, 0],  # n
            [1, 1, 1, 1, 1, 0, 1, 0],  # O
            [1, 1, 0, 0, 1, 1, 1, 0],  # P
            [1, 1, 1, 0, 0, 1, 1, 0],  # q
            [0, 0, 0, 0, 1, 1, 0, 0],  # r
            [1, 0, 1, 1, 0, 1, 1, 0],  # S
            [0, 0, 0, 1, 1, 1, 1, 0],  # t
            [0, 1, 1, 1, 1, 0, 1, 0],  # U
            [0, 1, 1, 1, 1, 0, 1, 0],  # V (похож на U)
            [0, 0, 0, 0, 0, 0, 0, 0],  # W (не отображается)
            [0, 1, 1, 0, 1, 1, 1, 0],  # X (похож на H)
            [0, 1, 1, 1, 0, 1, 1, 0],  # y
            [1, 1, 0, 1, 1, 1, 0, 0],  # Z (похож на 2)
            
            # Специальные символы
            [0, 0, 0, 0, 0, 1, 0, 0],  # Минус
            [0, 0, 0, 0, 0, 0, 0, 1],  # Точка
            [1, 1, 0, 0, 0, 1, 1, 0],  # Звезда
            [0, 0, 0, 1, 0, 0, 0, 0],  # Подчеркивание
        ]

    def display_digit(self, num, position):
        """
        Отображает одну цифру на указанном разряде.
        :param num: Цифра для отображения (0-35: 0-9, A-Z, пробел, минус, точка, звезда, подчеркивание).
        :param position: Позиция разряда (0-3).
        """
        if num < 0 or num >= len(self.digits):  # Проверяем, что индекс в пределах списка
            return  # Игнорируем недопустимые значения
        
        for pin in self.digit_pins:
            pin.value(1)  # Выключаем все разряды
        self.digit_pins[position].value(0)  # Включаем нужный разряд
        
        for i in range(8):  # Устанавливаем сегменты
            self.segments[i].value(self.digits[num][i])

    def number(self, num_str, zeros=True, duration=1):
        """
        Отображает строку на дисплее.
        :param num_str: Строка для отображения (например, "12.34" или "-56.78").
        :param zeros: Если True, отображает ведущие нули.
        :param duration: Время отображения числа в секундах.
        """
        start_time = utime.time()  # Запоминаем время начала

        # Проверяем, есть ли минус в строке
        is_negative = num_str.startswith('-')
        if is_negative:
            num_str = num_str[1:]  # Убираем минус из строки

        # Проверяем, есть ли точка в строке
        is_decimal = '.' in num_str

        # Если zeros=True, добавляем ведущие нули
        if zeros and not is_decimal:
            num_length = len(num_str)
            if num_length < 4:
                num_str = '0' * (4 - num_length) + num_str  # Добавляем ведущие нули

        # Дополняем строку до 4 символов (если нужно)
        if len(num_str) < 4:
            num_str = num_str + ' ' * (4 - len(num_str))  # Ручное дополнение пробелами

        while utime.time() - start_time < duration:  # Отображаем строку в течение duration секунд
            i = 0
            position = 0  # Позиция разряда

            # Отображаем минус, если число отрицательное
            if is_negative:
                self.display_digit(47, position)  # Минус
                position += 1

            while i < len(num_str) and position < 4:
                char = num_str[i]
                if char == '.':
                    # Если точка, используем паттерн с точкой для предыдущей цифры
                    if i > 0:
                        prev_char = num_str[i - 1]
                        if prev_char.isdigit():
                            digit = int(prev_char)
                            self.display_digit(digit, position - 1)
                            self.segments[7].value(1)  # Включаем точку
                    i += 1  # Пропускаем точку
                else:
                    if char.isdigit():
                        digit = int(char)
                        # Для дробных чисел всегда отображаем нули после точки
                        if is_decimal and i > num_str.find('.'):
                            self.display_digit(digit, position)
                        else:
                            self.display_digit(digit, position)
                    elif char.isalpha():
                        # Преобразуем букву в индекс в списке паттернов
                        index = ord(char.upper()) - ord('A') + 21
                        self.display_digit(index, position)
                    else:
                        # Обработка специальных символов
                        if char == ' ':
                            self.display_digit(10, position)  # Пробел
                        elif char == '-':
                            self.display_digit(47, position)  # Минус
                        elif char == '.':
                            self.display_digit(48, position)  # Точка
                        elif char == '*':
                            self.display_digit(40, position)  # Звезда
                        elif char == '_':
                            self.display_digit(50, position)  # Подчеркивание
                    i += 1
                    position += 1  # Переходим к следующему разряду
                utime.sleep_ms(5)  # Задержка для мультиплексирования
                self.clear()  # Очищаем дисплей перед следующим разрядом

    def clear(self):
        """Очищает дисплей (выключает все сегменты)."""
        for pin in self.digit_pins:
            pin.value(1)  # Выключаем все разряды
        for pin in self.segments:
            pin.value(0)  # Выключаем все сегменты

    def scroll_text(self, text, delay=0.2):
        """
        Отображает текст с эффектом бегущей строки.
        :param text: Текст для отображения.
        :param delay: Задержка между сдвигами текста.
        """
        text_length = len(text)
        for i in range(text_length + 4):  # +4 для полного исчезновения текста
            display_text = text[max(0, i-4):i]  # Вырезаем часть текста для отображения
            # Вручную дополняем строку пробелами до 4 символов
            while len(display_text) < 4:
                display_text += ' '
            self.number(display_text, duration=delay)  # Отображаем текст

    def blink_text(self, text, times=3, delay=0.5):
        """
        Отображает текст с эффектом мигания.
        :param text: Текст для отображения.
        :param times: Количество миганий.
        :param delay: Задержка между миганиями.
        """
        for _ in range(times):
            self.number(text, duration=delay)
            self.clear()
            utime.sleep(delay)
