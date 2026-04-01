import requests
import xml.etree.ElementTree as ET

# Extracting exchange rates of the day
def get_bnr_rates():
    try:
        # Official URL for exchange rates
        url = "https://www.bnr.ro/nbrfxrates.xml"
        response = requests.get(url)
        tree = ET.fromstring(response.content)

        namespace = {'ns': 'http://www.bnr.ro/xsd'}

        rates = {}

        for rate in tree.findall('.//ns:Rate', namespace):
                currency = rate.get('currency')
                if currency in ['EUR', 'USD']:
                    rates[currency] = float(rate.text)
        return rates
    except Exception as e:
        print(f"Eroare BNR: {e}")
        # Backup values
        return {'EUR': 4.97, 'USD': 4.60}