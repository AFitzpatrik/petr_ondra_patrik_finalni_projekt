import requests


def get_country_info(country_name):
    """
    Provede dotaz na restcountries API na informace o zadaném státě.
    Vrací slovník:{'capital': ... , 'population': ..., 'language': ..., 'flag': ..., 'currency': ..., 'region': ..., 'area': ...}.
    Při chybě vrací None.
    """

    try:
        url = f"https://restcountries.com/v3.1/name/{country_name}?fullText=true"
        response = requests.get(url, timeout=5)
        data = response.json()

        if response.status_code == 200 and isinstance(data, list) and data:
            country_data = data[0]

            capital = country_data.get('capital', ['Neznámé'])[0]
            population = country_data.get('population', 'Neznámá')

            if 'languages' in country_data:
                languages = ', '.join(country_data['languages'].values())
            else:
                languages = 'Neznámé'
            #language = '. '.join(country_data.get('languages', {}).values()) if 'languages' in country_data else 'Neznámé'

            if 'flags' in country_data and 'svg' in country_data['flags']:
                flag = country_data['flags']['svg']
            else:
                flag = None

            if 'currencies' in country_data:
                currency_obj = list(country_data['currencies'].values())[0]
                currency = f"{currency_obj.get('name')} ({currency_obj.get('symbol')})"
            else:
                currency = 'Neznámá'

            if 'region' in country_data:
                region = country_data['region']
            else:
                region = 'Neznámý'

            if 'area' in country_data:
                area = round(country_data['area'])
            else:
                area = 'Neznámá'

            return {
                'capital': capital,
                'population': population,
                'languages': languages,
                'flag': flag,
                'currency': currency,
                'region': region,
                'area': area
            }


    except Exception as e:
        print(f"Chyba při načítání dat o státu: {country_name}: {e}")

    return None








