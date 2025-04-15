import requests
import json

def get_country_info():
    country_name = input("Введіть назву країни: ").strip()

    if not country_name:
        print("Помилка: назва країни не може бути порожньою.")
        return

    url = f"https://restcountries.com/v3.1/name/{country_name}"

    try:
        response = requests.get(url)
        response.raise_for_status()

        country_data = response.json()

        if isinstance(country_data, list) and len(country_data) > 0:
            # Спробуємо знайти точний збіг за common name
            matched_country = None
            for c in country_data:
                if c.get("name", {}).get("common", "").lower() == country_name.lower():
                    matched_country = c
                    break
            if not matched_country:
                matched_country = country_data[0]  # fallback — перший запис

            name = matched_country.get("name", {}).get("common", "Невідома назва")
            capital = matched_country.get("capital", ["Невідома столиця"])[0]
            region = matched_country.get("region", "Невідомий регіон")

            print("\nІнформація про країну:")
            print(f"Назва: {name}")
            print(f"Столиця: {capital}")
            print(f"Регіон: {region}")
        else:
            print("Країну не знайдено. Перевірте правильність написання.")

    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 404:
            print("Країну не знайдено. Перевірте правильність написання.")
        else:
            print("HTTP помилка:", http_err)
    except requests.exceptions.RequestException as e:
        print("Помилка при запиті:", e)
    except json.JSONDecodeError as e:
        print("Помилка при обробці відповіді:", e)

get_country_info()
