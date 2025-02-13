import json


def load_data(file_path):
    """Lädt eine JSON-Datei"""
    with open(file_path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def print_animal_info(data):
    """
    Gibt für jedes Tier in den Daten folgende Informationen aus (falls vorhanden):
      - Name
      - Diet
      - Der erste Eintrag aus der Liste 'locations'
      - Type
    """
    for animal in data:
        if 'name' in animal:
            print(f"Name: {animal['name']}")
        if 'diet' in animal:
            print(f"Diet: {animal['diet']}")
        if 'locations' in animal and isinstance(animal['locations'], list) and animal['locations']:
            print(f"Location: {animal['locations'][0]}")
        if 'type' in animal:
            print(f"Type: {animal['type']}")
        print()  # Leerzeile zur Trennung


def generate_animals_output(data):
    """
    Generiert einen String mit den Informationen der Tiere, wobei für jedes Tier:
      - Name, Diet, erster Location-Eintrag und Type (falls vorhanden)
      - mit Zeilenumbrüchen formatiert
    """
    output = ""
    for animal in data:
        if 'name' in animal:
            output += f"Name: {animal['name']}\n"
        if 'diet' in animal:
            output += f"Diet: {animal['diet']}\n"
        if 'locations' in animal and isinstance(animal['locations'], list) and animal['locations']:
            output += f"Location: {animal['locations'][0]}\n"
        if 'type' in animal:
            output += f"Type: {animal['type']}\n"
        output += "\n"  # Leerzeile als Trenner
    return output


def create_html(template_path, animals_info, output_path):
    """
    Liest das HTML-Template aus template_path, ersetzt den Platzhalter
    __REPLACE_ANIMALS_INFO__ mit dem animals_info-String und speichert
    das Ergebnis in output_path.
    """
    with open(template_path, "r", encoding="utf-8") as file:
        template = file.read()

    final_html = template.replace("__REPLACE_ANIMALS_INFO__", animals_info)

    with open(output_path, "w", encoding="utf-8") as file:
        file.write(final_html)


if __name__ == '__main__':
    # Schritt 1: JSON-Daten laden und in der Konsole ausgeben
    animals_data = load_data('animals_data.json')
    print_animal_info(animals_data)

    # Schritt 2: Tiere-Informationen als String generieren
    animals_info = generate_animals_output(animals_data)

    # Schritt 3: HTML-Template laden, den Platzhalter ersetzen und in animals.html schreiben
    create_html("animals_template.html", animals_info, "animals.html")

    print("Die Datei animals.html wurde erfolgreich erstellt.")
