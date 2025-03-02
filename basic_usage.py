from quaddisplay import QuadDisplay
# Пример использования
segment_pins = [15, 14, 13, 12, 11, 10, 9, 8]  # Пины для сегментов
digit_pins = [16, 17, 18, 19]  # Пины для разрядов

display = QuadDisplay(segment_pins, digit_pins)

# бесконечный цикл для отображения чисел
while True:
    # Отображаем число 256 с ведущими нулями в течение 5 секунд
    display.display_number(256, leading_zeros=True, duration=5)
    
    # Отображаем число 257 без ведущих нулей в течение 5 секунд
    display.display_number(257, leading_zeros=False, duration=5)
