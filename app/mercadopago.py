import mercadopago
import os

class Payment:
    def __init__(self):
        self.__PUBLIC_KEY = os.environ["PAGSEG_PUBLIC_KEY"]
        self.__ACCESS_TOKEN = os.environ["PAGSEG_ACCESS_TOKEN"]

    @staticmethod
    def __format_request(payment_dictionary, freight_value):
        preferences = {"items": []}
        for key, value in payment_dictionary.items():
            preferences["items"].append(
                {"title": value["name"],
                 "quantity": value["quantity"],
                 "currence_id": "BRL",
                 "unit_price": value["price"]})
        freight_service = {
            "title": "frete",
            "quantity": 1,
            "currence_id": "BRL",
            "unit_price": freight_value}
        preferences["items"].append(freight_service)
        return preferences

    def payment(self, payment_data, freight_value):
        preference_data = self.__format_request(payment_data, freight_value)
        try:
            sdk = mercadopago.SDK(self.__ACCESS_TOKEN)
            preference_response = sdk.preference().create(preference_data)
            print(preference_response)
            url = preference_response["response"]["init_point"]
        except Exception as e:
            print(e)
            url = "/"
        return url
