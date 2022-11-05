import random


class PasswordGenerator:
    """This class is for generating password."""
    UPPER_CASE_LETTER = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
                         'S', 'T', 'U', 'V', 'W', 'X', 'Y']
    LOWER_CASE_LETTER = list(map(lambda letter: letter.lower(), UPPER_CASE_LETTER))
    DIGITS = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
    SYMBOLS = ['`', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+', '-', '=', '{', '}', '[', ']', ':',
               ';', '|', '\\', '<', '>', '?', ',', '.', '/', '`', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_',
               '+', '-', '=', '{', '}', '[', ']', ':', ';', '|', '<', '>', '?', ',', '.', '/']
    COMBINATION = []
    COMBINATION.extend(UPPER_CASE_LETTER)
    COMBINATION.extend(LOWER_CASE_LETTER)
    COMBINATION.extend(DIGITS)
    COMBINATION.extend(SYMBOLS)

    def __init__(self, password_length, upper=True, lower=True, nums=True, symb=True):
        self.__password_length = password_length
        self.upper = upper
        self.lower = lower
        self.nums = nums
        self.symb = symb
        self.__password = self.password_generate()

    def password_generate(self):
        i = 0
        password = []
        if self.__password_length >= 4:
            if self.upper == "True":
                password.append(random.choice(self.UPPER_CASE_LETTER))
                i += 1
            if self.lower == "True":
                password.append(random.choice(self.LOWER_CASE_LETTER))
                i += 1
            if self.nums == "True":
                password.append(random.choice(self.DIGITS))
                i += 1
            if self.symb == "True":
                password.append(random.choice(self.SYMBOLS))
                i += 1
            if self.__password_length >= 4:
                while i < self.__password_length:
                    password.append(random.choice(self.COMBINATION))
                    i += 1
            random.shuffle(password)
        else:
            for i in range(self.__password_length):
                password.append(random.choice(self.COMBINATION))
        return "".join(password)
