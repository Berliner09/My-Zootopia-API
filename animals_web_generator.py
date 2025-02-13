import json

def load_data(file_path):
    """Lädt eine JSON-Datei"""
    with open(file_path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def print_animal_info(data):
    for animal in data:
        # Prüft und druckt Name, falls vorhanden
        if 'name' in animal:
            print(f"Name: {animal['name']}")

        # Prüft und druckt Diet, falls vorhanden
        if 'diet' in animal:
            print(f"Diet: {animal['diet']}")

        # Prüft, ob "locations" existiert, ob es eine Liste ist und ob sie mindestens ein Element enthält
        if 'locations' in animal and isinstance(animal['locations'], list) and animal['locations']:
            print(f"Location: {animal['locations'][0]}")

        # Prüft und druckt Type, falls vorhanden
        if 'type' in animal:
            print(f"Type: {animal['type']}")

        # Leerzeile zur Trennung der Einträge
        print()


# Main-Bereich: Daten laden und ausgeben
if __name__ == '__main__':
    animals_data = load_data('animals_data.json')
    print_animal_info(animals_data)
