def roman_to_int(roman):
    roman_numerals = {
        'I': 1, 'V': 5, 'X': 10,
        'L': 50, 'C': 100, 'D': 500,
        'M': 1000
    }
    
    total = 0
    prev_value = 0
    
    for symbol in reversed(roman):
        value = roman_numerals.get(symbol)
        if value is None:
            raise ValueError("Некорректное римское число")
        if value < prev_value:
            total -= value
        else:
            total += value
        prev_value = value
    return total

def int_to_roman(num):
    if num <= 0:
        raise ValueError("Римские числа не используются для нулей или отрицательных чисел")
    roman_map = [
        (1000, 'M'), (900, 'CM'), (500, 'D'),
        (400, 'CD'), (100, 'C'), (90, 'XC'),
        (50, 'L'), (40, 'XL'), (10, 'X'),
        (9, 'IX'), (5, 'V'), (4, 'IV'),
        (1, 'I')
    ]
    result = ''
    for value, symbol in roman_map:
        while num >= value:
            result += symbol
            num -= value
    return result

def main():
    input_str = input("Введите выражение (например, 'VI - II'): ").strip()
    try:
        parts = input_str.split()
        if len(parts) != 3:
            raise ValueError("Некорректный формат ввода")
        num1_str, op, num2_str = parts
    except Exception as e:
        print("Ошибка ввода:", e)
        return

    try:
        num1 = roman_to_int(num1_str)
        num2 = roman_to_int(num2_str)
    except ValueError:
        print("Некорректное римское число.")
        return

    try:
        if op == '+':
            result = num1 + num2
        elif op == '-':
            result = num1 - num2
        elif op == '*':
            result = num1 * num2
        elif op == '/':
            if num2 == 0:
                raise ZeroDivisionError("Деление на ноль невозможно.")
            result = int(num1 / num2)
        else:
            raise ValueError("Неизвестная операция")
    except ZeroDivisionError as e:
        print(e)
        return

    if result <= 0:
        print("Результат не может быть отрицательным или нулём для римских чисел.")
        return

    try:
        roman_result = int_to_roman(result)
        print(roman_result)
    except ValueError as e:
        print(e)

if __name__ == "__main__":
    main()
