import requests
import hashlib


class PasswordValidator:
    def __init__(self, password):
        self.__password = password
        self.__upper_case_letter = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
                                    'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y']
        self.__lower_case_letter = list(map(lambda letter: letter.lower(), self.__upper_case_letter))
        self.__digits = [str(x) for x in range(0, 10)]
        self.__symbols = ['`', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+', '-', '=', '{', '}', '[', ']',
                          ':',
                          ';',
                          '|', '\\', '<', '>', '?', ',', '.', '/', '`', '!', '@', '#', '$', '%', '^', '&', '*', '(',
                          ')', '_',
                          '+',
                          '-', '=', '{', '}', '[', ']', ':', ';', '|', '<', '>', '?', ',', '.', '/']
        self.__combination = []
        self.__combination.extend(self.__upper_case_letter)
        self.__combination.extend(self.__lower_case_letter)
        self.__combination.extend(self.__digits)
        self.__combination.extend(self.__symbols)

    def password_validation(self):
        if (
                len(self.__password) >= 8
                and any(sign for sign in self.__password if sign in self.__upper_case_letter)
                and any(sign for sign in self.__password if sign in self.__lower_case_letter)
                and any(sign for sign in self.__password if sign in self.__digits)
                and any(sign for sign in self.__password if sign in self.__symbols)
        ):
            return f"You password is strong"
        return f"You password is too weak"

    def password_seen_in_data_branch(self):
        password = hashlib.sha1()
        password.update(bytes(self.__password, 'utf-8'))
        password_hex = password.hexdigest()
        hex = password_hex[5:].upper()
        hex_len_5 = password_hex[:5]
        url = f"https://api.pwnedpasswords.com/range/{hex_len_5}"
        headers = {"Accept": "application/vnd.haveibeenpwned.v3+json",
                   "hibp-api-key": "a9887058081a491d9f9339c4b769f8ef"}
        r = requests.get(url, verify=True, headers=headers)
        if r.status_code != 200:
            return f"Can't check"
        else:
            response_text = r.text.split("\n")
            if hex in r.text:
                for pwd in response_text:
                    if hex in pwd:
                        index = pwd.index(":")
                        how_many_times = pwd[index + 1:]
                        return f"This password has been seen {int(how_many_times)} times before"
            else:
                return "no pwnage found!"


a = PasswordValidator('kamil1')
print(a.password_seen_in_data_branch())
