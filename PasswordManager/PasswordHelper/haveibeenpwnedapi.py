import requests


class HaveIBeenPwned:
    def __init__(self, email):
        self.email = email

    def get_pwned_info(self):
        url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{self.email}"
        headers = {"Accept": "application/vnd.haveibeenpwned.v3+json",
                   "hibp-api-key": "a9887058081a491d9f9339c4b769f8ef"}
        r = requests.get(url, verify=True, headers=headers)
        pwned_list = []
        if r.status_code == 404:
            return f"Haven't been pwned"
        elif r.status_code == 200:
            response_dict = r.json()
            for n in response_dict:
                pwned_list.append(n['Name'])
            return f"Have been pwned {len(response_dict)} times on {pwned_list}"
