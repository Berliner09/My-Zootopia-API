# animals_web_generator.py
import data_fetcher  # Importiert unsere eigene Modul
import sys           # Für Fehlerausgaben und sys.exit

def print_animal_info(data):
    """
    Gibt ausgewählte Tierinformationen (unformatiert) in der Konsole aus.
    Nützlich für schnelles Debugging.
    """
    if not data:
        print("Keine Daten zum Anzeigen vorhanden.")
        return

    print("\n--- Abgerufene Tierdaten (Konsolenausgabe) ---")
    for animal in data:
        print(f"Name: {animal.get('name', 'N/A')}")
        # Sicherer Zugriff auf verschachtelte Daten
        characteristics = animal.get('characteristics', {})
        print(f"  Diet: {characteristics.get('diet', 'N/A')}")
        print(f"  Type: {characteristics.get('type', 'N/A')}")
        # Nimm die erste Location, falls vorhanden
        locations = animal.get('locations', [])
        location = locations[0] if locations else 'N/A'
        print(f"  Location: {location}")
        print("-" * 20) # Trennlinie

def serialize_animal(animal_obj):
    """
    Serialisiert ein einzelnes Tier-Objekt in ein HTML-Listenelement (`<li>`).
    Greift sicher auf Daten zu und verwendet Standardwerte bei fehlenden Keys.
    """
    output = '            <li class="cards__item">\n' # Einrückung für Lesbarkeit im HTML
    output += f'              <div class="card__title">{animal_obj.get("name", "Unbekanntes Tier")}</div>\n'
    output += '              <p class="card__text">\n'

    characteristics = animal_obj.get('characteristics', {})
    diet = characteristics.get('diet', 'N/A')
    output += f'                <strong>Diet:</strong> {diet}<br/>\n'

    locations = animal_obj.get('locations', [])
    location = locations[0] if locations else 'N/A'
    output += f'                <strong>Location:</strong> {location}<br/>\n'

    animal_type = characteristics.get('type') # Kein Standardwert nötig, da wir unten prüfen
    if animal_type: # Nur hinzufügen, wenn 'type' vorhanden und nicht leer ist
        output += f'                <strong>Type:</strong> {animal_type}<br/>\n'

    # Optional: Weitere interessante Infos hinzufügen, falls vorhanden
    lifespan = characteristics.get('lifespan')
    if lifespan:
         output += f'                <strong>Lifespan:</strong> {lifespan}<br/>\n'

    output += '              </p>\n'
    output += '            </li>\n'
    return output

def generate_animals_output(data):
    """
    Generiert einen HTML-String mit Listenelementen für jedes Tier in der Liste.
    """
    if not data:
        return "" # Leerer String, wenn keine Daten vorhanden sind

    # Nutze List Comprehension und join für Effizienz
    html_list_items = [serialize_animal(animal) for animal in data]
    return "".join(html_list_items)

def create_html(template_path, animals_info_html, output_path):
    """
    Liest das HTML-Template, ersetzt den Platzhalter und schreibt die finale HTML-Datei.
    Gibt True bei Erfolg zurück, False bei Fehlern.
    """
    try:
        with open(template_path, "r", encoding="utf-8") as file:
            template = file.read()
    except FileNotFoundError:
        print(f"FEHLER: Template-Datei '{template_path}' nicht gefunden.", file=sys.stderr)
        return False
    except IOError as e:
        print(f"FEHLER beim Lesen der Template-Datei '{template_path}': {e}", file=sys.stderr)
        return False

    # Ersetze den Platzhalter durch die generierten HTML-Listenelemente
    final_html = template.replace("__REPLACE_ANIMALS_INFO__", animals_info_html)

    try:
        with open(output_path, "w", encoding="utf-8") as file:
            file.write(final_html)
        return True # Erfolg signalisieren
    except IOError as e:
        print(f"FEHLER beim Schreiben der HTML-Datei '{output_path}': {e}", file=sys.stderr)
        return False

# Hauptausführungsblock
if __name__ == '__main__':
    # Benutzer nach einem Tiernamen fragen (mit Validierung)
    animal_name = ""
    while not animal_name:
        animal_name = input("Bitte gib einen Tiernamen ein (z.B. Tiger, Dog, Fox): ").strip()
        if not animal_name:
            print("Die Eingabe darf nicht leer sein.")

    print(f"Suche nach '{animal_name}'...")

    # Daten über den data_fetcher abrufen
    # Hier ist keine explizite Fehlerbehandlung mehr nötig, da fetch_data
    # im Fehlerfall eine leere Liste zurückgibt und Fehler auf stderr druckt.
    animals_data = data_fetcher.fetch_data(animal_name)

    # HTML-Inhalt generieren oder Fehlermeldung erstellen
    animals_info_html = ""
    if animals_data:
        # Wenn Daten vorhanden, optional in Konsole ausgeben und HTML generieren
        # print_animal_info(animals_data) # Auskommentieren, wenn nicht benötigt
        animals_info_html = generate_animals_output(animals_data)
        print(f"{len(animals_data)} Tier(e) gefunden und verarbeitet.")
    else:
        # Fehlermeldung für das HTML (Milestone 3)
        # Wichtig: Der Platzhalter wird trotzdem ersetzt, aber eben mit dieser Meldung.
        animals_info_html = f'            <h2>Das Tier "{animal_name}" wurde nicht gefunden oder es gab einen Fehler beim Abrufen der Daten.</h2>\n'
        print(f"Keine Daten für '{animal_name}' gefunden oder Fehler beim Abruf.")


    # HTML-Datei erstellen
    template_file = "animals_template.html"
    output_file = "animals.html"
    if create_html(template_file, animals_info_html, output_file):
        print(f"Webseite wurde erfolgreich in '{output_file}' generiert.")
    else:
        # Bei Fehlern beim Schreiben der Datei wird das Programm beendet.
        print("Die Webseite konnte nicht erstellt werden.", file=sys.stderr)
        sys.exit(1) # Beendet das Skript mit einem Fehlercode