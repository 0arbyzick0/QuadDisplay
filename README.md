### QuadDisplay

Библиотека для управления 4-битными 7-сегментными дисплеями на микроконтроллерах типа RPi с использованием MicroPython. Я сделал эту библиотеку с deepseek так что не ожидайте самого лучшего результата, сделано для простоты и с любовью. Я тестировал только на Raspberry Pi Pico но он должен работать на всех микроконтроллерах типа RPi ( я думаю ). Библиотека использует мультиплексинг ( комбинирование нескольких сигналов в 1 ) и большое разнообразие функций
\\
QuadDisplay - a library to control 4 bit 7 segment displays on RPi like microcontrollers using MicroPython. I made this library with deepseek soooo dont expect that much quality, made for easier use and with love. I tested this only on Raspberry Pi Pico, but it should work on all RPi like microncontrollers ( i think ). Library uses multiplexing ( combining multiple signals into one ) and a bunch of other features!

## Установка / Installing

Скопируй файл `quaddisplay.py` в папку lib на твоём микроконтроллере
//
Copy `quaddisplay.py` into the folder lib on your microcontroller

## Использование / Usage

Я подключал по этой схеме, её очень легко понять:
\\
I connected by this circuit, its very easy to understand:
![image](https://github.com/user-attachments/assets/215243b6-63e7-4b07-b2db-61c710d80405)

и подсоедини пины по таблице:
and connected them like so:
| Raspberry Pi Pico | Пин / Pins |
--------------------|------
| GPIO 16	| 1 (первая цифра / first digit) |
| GPIO 17	| 2 (вторая цифра / second digit) |
| GPIO 18	| 3 (третья цифра / third digit) |
| GPIO 19	| 4 (четвёртая цифра / fourth digit) |
| GPIO 15	| a (верх / top) |
| GPIO 14	| b (верхний правый / upper right) |
| GPIO 13	| c (нижний правый / lower right) |
| GPIO 12	| d (нижний / bottom) |
| GPIO 11	| e (нижний левый / lower left) |
| GPIO 10	| f (верхний левый / upper left) |
| GPIO 9	| g (середина / middle) |
| GPIO 8	| p (точка / point) |

## Пример / Example

```python
from quaddisplay import QuadDisplay
import utime

# Пины для сегментов (a, b, c, d, e, f, g, dp) // pins for segments
segment_pins = [15, 14, 13, 12, 11, 10, 9, 8]
# Пины для разрядов (Digit 1, Digit 2, Digit 3, Digit 4) // pins for digits
digit_pins = [16, 17, 18, 19]

# Создаем объект дисплея // display object
display = QuadDisplay(segment_pins, digit_pins)

# Бесконечный цикл для отображения чисел и текста // infinite cycle for showing numbers and text
while True:
    display.number("123", zeros=True, duration=2)  # Отображаем 123 с ведущими нулями // showing 123 with zeroes
    display.number("0123", zeros=False, duration=2) # Отображаем 0123 как 123 // showing 0123 as 123
    display.number("12.34", duration=2)            # Отображаем 12.34 // showing 12.34
    display.number("-56.78", duration=2)           # Отображаем -56.78 // showing -56.78
    
    # Анимации
    display.scroll_text("HELLO", delay=0.2)        # Бегущая строка // text scrolling
    display.blink_text("TEST", times=3, delay=0.5)  # Мигание текста // text blinking
    
    # Отображение текста
    display.number("ABCD", duration=3)             # Отображаем текст // showing text
```
## Функции / Functions
# QuadDisplay(пины сегментов / segment pins, пины разрядов // digit pins)
- пины сегментов // segment pins  = можно сделать как в примере ( лист ) или просто написать лист в самой функции // pins for segments
- пины разрядов // digit pins = тоже самое как пины сегментов, но для пинов разрядов // pins for digits

# QuadDisplay.number(num, zeros=True, duration=1)
- num = в строку можно ввести любое число до 4-х цифр или любое слово до 4-х букв // a str of number/word
- zeros=True = будут ли показываться ведущие нули (если False, тогда 0123 = 123) [я починил её!!!] // show zeroes (if True, 12 = 0012) [i fixed it!]
- duration=1 = время на которое число/слово будет показываться на экране [опять же функция странная, но работает] // time the number/words will stay on the screen [ a strange function but it works ]

# QuadDisplay.scroll_text(text, delay=0.2)
- text = анимация строки в которой слово или число будет бежать по строке // a str of a word/number
- delay = задержка перед переключением буквы/цифры // delay between switching to the next number/letter

# QuadDisplay.blink_text(text, times=3, delay=0.5)
- text = анимация строки в которой слово или число будет мигать // a str of a word/number
- times = количество миганий // how many times to blink
- delay = задержка между миганиями // delay between blinks

# QuadDisplay.clear()
- очищает все разряды и сегменты // clears all digits and segments

надеюсь вам будет полезно! // hope this helps!
