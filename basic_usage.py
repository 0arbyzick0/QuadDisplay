from quaddisplay import QuadDisplay
import utime

# Пины для сегментов (a, b, c, d, e, f, g, dp)
segment_pins = [15, 14, 13, 12, 11, 10, 9, 8]
# Пины для разрядов (Digit 1, Digit 2, Digit 3, Digit 4)
digit_pins = [16, 17, 18, 19]

# Создаем объект дисплея
display = QuadDisplay(segment_pins, digit_pins)

# Бесконечный цикл для отображения чисел и текста
while True:
    display.number("123", zeros=True, duration=2)  # Отображаем 123 без ведущих нулей
    display.number("023", zeros=False, duration=2) # Отображаем 0123 как 123
    display.number("12.34", duration=2)            # Отображаем 12.34
    display.number("-56.78", duration=2)           # Отображаем -56.78
    
    # Анимации
    display.scroll_text("123456789", delay=0.2)        # Бегущая строка
    display.blink_text("TEST", times=3, delay=0.5) # Мигание текста
    
    # Отображение текста
    display.number("ABCD", duration=3)             # Отображаем текст
