# data_fetcher.py
import requests
import os
import sys  # Für Fehlermeldungen auf stderr
from dotenv import load_dotenv

# Lade Umgebungsvariablen aus der .env Datei.
# Wichtig: Muss vor dem Zugriff auf os.getenv erfolgen.
load_dotenv()

# Hole den API-Schlüssel aus den Umgebungsvariablen.
API_KEY = os.getenv('API_KEY')
# Definiere die Basis-URL für die API.
API_URL = 'https://api.api-ninjas.com/v1/animals'

def fetch_data(animal_name):
    """
    Ruft Tierdaten für 'animal_name' von der API-Ninjas API ab.

    Args:
        animal_name (str): Der Name des gesuchten Tieres.

    Returns:
        list: Eine Liste von Tier-Dictionaries bei Erfolg.
              Gibt eine leere Liste zurück, wenn der API-Schlüssel fehlt,
              die Anfrage fehlschlägt oder keine Tiere gefunden werden.
    """
    if not API_KEY:
        # Gibt eine Fehlermeldung auf stderr aus, damit sie nicht
        # mit normalen Ausgaben vermischt wird.
        print("FEHLER: API_KEY wurde nicht in der .env Datei gefunden oder geladen.", file=sys.stderr)
        return [] # Leere Liste signalisiert dem Aufrufer ein Problem/keine Daten

    headers = {'X-Api-Key': API_KEY}
    params = {'name': animal_name}

    try:
        # Sende die GET-Anfrage an die API.
        response = requests.get(API_URL, headers=headers, params=params, timeout=10) # Timeout hinzufügen
        # Überprüfe auf HTTP-Fehler (z.B. 401, 403, 404, 5xx).
        response.raise_for_status()

        # Wandle die JSON-Antwort in eine Python-Liste um.
        # Die API gibt eine leere Liste zurück, wenn nichts gefunden wurde.
        data = response.json()
        return data

    except requests.exceptions.HTTPError as http_err:
        # Spezifische Behandlung von HTTP-Fehlern (z.B. falscher API-Key -> 401)
        print(f"HTTP Fehler beim Abrufen von '{animal_name}': {http_err} (Status Code: {response.status_code})", file=sys.stderr)
        return []
    except requests.exceptions.Timeout:
        print(f"Timeout Fehler beim Abrufen von '{animal_name}'. Die API hat nicht rechtzeitig geantwortet.", file=sys.stderr)
        return []
    except requests.exceptions.RequestException as req_err:
        # Fängt andere requests-Fehler ab (z.B. Netzwerkprobleme).
        print(f"Netzwerkfehler beim Abrufen von '{animal_name}': {req_err}", file=sys.stderr)
        return []
    except Exception as e:
        # Fängt unerwartete Fehler ab (z.B. Probleme beim JSON-Parsing, falls die API mal kein gültiges JSON sendet).
        print(f"Ein unerwarteter Fehler ist beim Abrufen von '{animal_name}' aufgetreten: {e}", file=sys.stderr)
        return []

# Optional: Kleiner Testblock für direktes Ausführen der Datei
if __name__ == '__main__':
    test_animals = ["Lion", "DoesNotExistXYZ123", "Dog"]
    for animal in test_animals:
        print(f"\n--- Teste fetch_data für: '{animal}' ---")
        results = fetch_data(animal)
        if results:
            print(f"Erfolg! {len(results)} Ergebnis(se) gefunden.")
            # Zeige nur Namen und Orte des ersten Ergebnisses
            first_result = results[0]
            print(f"  Name: {first_result.get('name', 'N/A')}")
            print(f"  Locations: {first_result.get('locations', [])}")
        else:
            print("Keine Ergebnisse gefunden oder Fehler aufgetreten (erwartet für 'DoesNotExistXYZ123').")