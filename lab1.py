import math


def get_tokens(expr):
    for i in "+-*/()|":                  # добавляем знаки вокруг пробелов, чтобы 
        expr = expr.replace(i, f" {i} ") # split() разрезал строку на токены 
    parts = expr.split()
    tokens = []
    for p in parts:
        if p == "floor":
            tokens.append(("FUNC", "floor"))
        elif p in "+-*/()|":
            tokens.append(("OPER", p))
        else:
            tokens.append(("NUM", float(p)))
            
    tokens.append(("END", "END")) #маркет конца выражения
    return tokens


def calculator(expr):
    
    tokens = get_tokens(expr)
    pos = 0

    def current(offset=0):   #текущий токен, не сдвигая позицию
        i = pos + offset
        return tokens[i] if i < len(tokens) else ("END", "END")

    def move():              #текущий токен + сдвиг позиции
        nonlocal pos
        token = current()
        pos += 1
        return token

    def check_brace(value):  #проверка на ожидаемую скобку
        token = move()
        if token[1] != value:
            raise ValueError(f"Ожидалось {value}, получено {token[1]}")
        return token

    def priority_1():
        # Приоретет 1: числа, скобки, floor, унарные + и -
        t_type, t_val = move()
        if t_type == "NUM":
            return t_val
        if t_val == "(":
            res = priority_4()
            check_brace(")")
            return res
        if t_val == "floor":
            check_brace("(")
            res = math.floor(priority_4())
            check_brace(")")
            return res                          
        if t_val == "-":
            return -priority_1()
        if t_val == "+":
            return priority_1()
        raise ValueError(f'Ошибка на: {t_val}')

    def priority_2():
        # Приоритет 2: * и /
        res = priority_1()
        while current()[1] in ("*", "/"):
            op = move()[1]
            next_res = priority_1()
            if op == "*":
                res *= next_res
            else:
                if next_res == 0:
                    raise ValueError("Деление на ноль")
                res /= next_res
        return res

    def priority_3():
        # Приоритет 3: + и -
        res = priority_2()
        while current()[1] in ("+", "-"):
            op = move()[1]
            next_res = priority_2()
            if op == "+":
                res += next_res
            else:
                res -= next_res
        return res                              

    def priority_4():
        # Приоритет 4: | - побитовое или
        res = priority_3()
        while current()[1] == "|":
            move()
            res = int(res) | int(priority_3())
        return res

    result = priority_4()

    # Проверка, вся ли строка разобрана
    if current()[0] != "END":
        raise ValueError(f"Лишние символы в конце")
    return result


expr = input("Введите выражение: ")
print("Ответ:", calculator(expr))
