
class Calculator:
    """
    Singleton Calculator instance performs basic calculations on numbers.

    Numbers can be given in various forms: as int, float, double or as string
    numbers, e.g. "123" or "1.600" or as Latin numbers "X", as single digit
    words: "three" (English, 3), "cinco" (Spanish, 5), "семь" (Russian, 7),
    "X" (Latin, 10) or "三" (Chinese, sān 3).

    See: https://sgra64.github.io/py-fun.github.io/src.calculator.html.
    """

    def add(_self, a, b):

        return _self._convert(a) + _self._convert(b)

    def sub(_self, a, b):
        
        return _self._convert(a) - _self._convert(b)

    def mul(_self, a, b):
       
        return _self._convert(a) * _self._convert(b)

    def div(_self, a, b):
        
        a = _self._convert(a)
        b = _self._convert(b)

        if b == 0:
            return float('inf')

        return a / b

    def factorize(_self, n):
      
        n = int(_self._convert(n))

        if n < 0:
            raise ValueError("Cannot factorize a negative number")

        factors = []
        divisor = 2

        while n > 1:
            while n % divisor == 0:
                factors.append(divisor)
                n //= divisor
            divisor += 1

        return factors

    def _convert(_self, value):
        """Convert supported number representations into numeric values."""

        if value is None:
            return 0

        if isinstance(value, (int, float)):
            return value

        if not isinstance(value, str):
            return 0

        value = value.strip().lower()

        if not value:
            return 0

        # Numeric strings
        try:
            number = float(value)
            return int(number) if number.is_integer() else number
        except ValueError:
            pass

        # Number words in different languages
        words = {
            "zero": 0, "one": 1, "two": 2, "three": 3,
            "four": 4, "five": 5, "six": 6, "seven": 7,
            "eight": 8, "nine": 9, "ten": 10,

            "null": 0, "eins": 1, "zwei": 2, "drei": 3,
            "vier": 4, "fünf": 5, "fuenf": 5,
            "sechs": 6, "sieben": 7, "acht": 8,
            "neun": 9, "zehn": 10,

            "uno": 1, "dos": 2, "tres": 3, "cuatro": 4,
            "cinco": 5, "seis": 6, "siete": 7,
            "ocho": 8, "nueve": 9, "diez": 10,

            "один": 1, "два": 2, "три": 3, "четыре": 4,
            "пять": 5, "шесть": 6, "семь": 7,
            "восемь": 8, "девять": 9, "десять": 10,

            "一": 1, "二": 2, "三": 3, "四": 4,
            "五": 5, "六": 6, "七": 7, "八": 8,
            "九": 9, "十": 10,
        }

        if value in words:
            return words[value]

        # Roman numerals
        roman = {
            "i": 1, "v": 5, "x": 10,
            "l": 50, "c": 100, "d": 500, "m": 1000
        }

        if all(char in roman for char in value):
            total = 0

            for i in range(len(value)):
                current = roman[value[i]]

                if i + 1 < len(value) and current < roman[value[i + 1]]:
                    total -= current
                else:
                    total += current

            return total

        # Unknown strings default to zero
        return 0

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        pass
