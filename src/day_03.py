def day_03a():
    total = 0
    with open("inputs/input_03.txt") as f:
        char = f.read(1)
        while char:
            if char != "m":
                char = f.read(1)
                continue
            char = f.read(1)
            if char != "u":
                continue
            char = f.read(1)
            if char != "l":
                continue
            char = f.read(1)
            if char != "(":
                continue

            num1 = ""
            while (char := f.read(1)) in "0123456789":
                num1 += char
            if char != "," or not num1:
                continue
            num2 = ""
            while (char := f.read(1)) in "0123456789":
                num2 += char
            if char != ")" or not num2:
                continue

            total += int(num1) * int(num2)
            char = f.read(1)

    return total


def day_03b():
    total = 0
    on = True
    with open("inputs/input_03.txt") as f:
        char = f.read(1)
        while char:
            if char == "m":
                char = f.read(1)
                if char != "u":
                    continue
                char = f.read(1)
                if char != "l":
                    continue
                char = f.read(1)
                if char != "(":
                    continue

                num1 = ""
                while (char := f.read(1)) in "0123456789":
                    num1 += char
                if char != "," or not num1:
                    continue
                num2 = ""
                while (char := f.read(1)) in "0123456789":
                    num2 += char
                if char != ")" or not num2:
                    continue

                if on:
                    total += int(num1) * int(num2)

            elif char == "d":
                char = f.read(1)
                if char != "o":
                    continue
                char = f.read(1)
                if char == "(":
                    char = f.read(1)
                    if char != ")":
                        continue

                    on = True

                elif char == "n":
                    char = f.read(1)
                    if char != "'":
                        continue
                    char = f.read(1)
                    if char != "t":
                        continue
                    char = f.read(1)
                    if char != "(":
                        continue
                    char = f.read(1)
                    if char != ")":
                        continue

                    on = False

            char = f.read(1)

    return total


if __name__ == "__main__":
    answer_03a = day_03a()
    print(answer_03a)
    answer_03b = day_03b()
    print(answer_03b)
