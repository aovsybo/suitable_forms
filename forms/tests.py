from rest_framework.test import APITestCase
from django.urls import reverse


class FunctionalTests(APITestCase):
    full_create_data = {
        "fields": {
            "name": "test_form_1",
            "nickname": "text",
            "creation_date": "date",
            "number": "phone",
            "mail": "email",
        }
    }
    full_get_data = {
        "nickname": "chester88",
        "creation_date": "10.10.2022",
        "number": "+7 912 214 81 92",
        "mail": "chester88@gmail.com",
    }

    def create_form(self, data):
        url = reverse('create-form')
        self.client.post(url, data, format='json')

    def get_form(self, data):
        url = reverse('get-form')
        return self.client.post(url, data, format='json').json()

    def test_existing_form(self):
        # Получение подходящей формы со всеми совпадающими полями
        self.create_form(self.full_create_data)
        response = self.get_form(self.full_get_data)
        correct = self.full_create_data["fields"]["name"]
        assert response == correct

    def test_other_existing_form(self):
        create_data = {
            "fields": {
                "name": "other_test_form",
                "profile_name": "text",
                "first_name": "text",
                "second_name": "text",
                "contact": "phone",
                "register_date": "date",
                "last_seen_date": "date",
            }
        }
        self.create_form(create_data)
        get_data = {
                "profile_name": "boyzya",
                "first_name": "Lex",
                "second_name": "Loster",
                "contact": "+7 912 412 54 12",
                "register_date": "11.11.2023",
                "last_seen_date": "2023-11-17",
            }
        response = self.get_form(get_data)
        correct = create_data["fields"]["name"]
        assert response == correct

    def test_non_existing_form(self):
        # Получение формы, не существующей в базе
        non_existing_data = {
                "first_name": "dave",
                "year": "01.01.2002",
            }
        response = self.get_form(non_existing_data)
        correct = {
            "first_name": "text",
            "year": "date"
        }
        assert response == correct

    def test_form_with_extra_fields(self):
        # Получение подходящей формы, где полей больше, чем в запрашиваемой форме
        self.create_form(self.full_create_data)
        # Получение словаря только из двух полей
        part_data = dict(list(self.full_get_data.items())[:2])
        response = self.get_form(part_data)
        correct = self.full_create_data["fields"]["name"]
        assert response == correct

    def form_with_wrong_field(self, wrong_field_name, wrong_field_value):
        # Получение подходящей формы, где где поле из параметров указано некорректно и считывается как текст
        # Сначала допускаем ошибку в указанном поле в запросе и безуспешно пробуем получить форму
        self.create_form(self.full_create_data)
        wrong_field_get_data = self.full_get_data
        wrong_field_get_data[wrong_field_name] = wrong_field_value
        response = self.get_form(wrong_field_get_data)
        correct = self.full_create_data["fields"]["name"]
        assert response != correct

        # Теперь создаем форму где некорректное поле - текст, и делаем запрос на эту форму
        wrong_field_create_data = self.full_create_data
        wrong_field_create_data["fields"][wrong_field_name] = "text"
        wrong_field_create_data["fields"]["name"] = "wrong_form_name"
        self.create_form(wrong_field_create_data)
        response = self.get_form(wrong_field_get_data)
        wrong_email_response = wrong_field_create_data["fields"]["name"]
        assert response == wrong_email_response

    def test_form_with_invalid_email(self):
        self.form_with_wrong_field("email", "wrong_email.com")

    def test_form_with_invalid_phone(self):
        self.form_with_wrong_field("phone", "+79991234567")

    def test_form_with_invalid_date(self):
        self.form_with_wrong_field("date", "25/11/2002")

    def test_same_types_different_names(self):
        different_names_data = {
            "fields": {
                "different_name": "defferent_names_test_form",
                "different_nickname": self.full_create_data["fields"]["nickname"],
                "different_creation_date": self.full_create_data["fields"]["creation_date"],
                "different_number": self.full_create_data["fields"]["number"],
                "different_mail": self.full_create_data["fields"]["mail"],
            }
        }
        self.create_form(different_names_data)
        response = self.get_form(self.full_get_data)
        correct = self.full_create_data["fields"]["name"]
        assert response != correct

    def test_different_types_same_names(self):
        different_types_data = {
            "fields": {
                "name": "defferent_types_test_form",
                "nickname": self.full_create_data["fields"]["mail"],
                "creation_date": self.full_create_data["fields"]["number"],
                "number": self.full_create_data["fields"]["creation_date"],
                "mail": self.full_create_data["fields"]["nickname"],
            }
        }
        self.create_form(different_types_data)
        response = self.get_form(self.full_get_data)
        correct = self.full_create_data["fields"]["name"]
        assert response != correct