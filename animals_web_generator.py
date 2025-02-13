import json


def load_data(file_path):
    """Lädt eine JSON-Datei"""
    with open(file_path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def print_animal_info(data):
    """
    Gibt die Tierinformationen (unformatiert) in der Konsole aus.
    Dabei werden, falls vorhanden, folgende Felder angezeigt:
      - Name
      - Diet (aus characteristics)
      - Type (aus characteristics)
      - Der erste Eintrag der locations-Liste
    """
    for animal in data:
        if 'name' in animal:
            print(f"Name: {animal['name']}")
        if 'characteristics' in animal:
            if 'diet' in animal['characteristics']:
                print(f"Diet: {animal['characteristics']['diet']}")
            if 'type' in animal['characteristics']:
                print(f"Type: {animal['characteristics']['type']}")
        if 'locations' in animal and isinstance(animal['locations'], list) and animal['locations']:
            print(f"Location: {animal['locations'][0]}")
        print()  # Leerzeile zur Trennung


def generate_animals_output(data):
    """
    Generiert einen HTML-formatierten String, in dem für jedes Tier ein Listenelement erzeugt wird.
    Folgende Felder werden (falls vorhanden) ausgegeben:
      - Name
      - Diet (aus characteristics)
      - Type (aus characteristics)
      - Der erste Eintrag der locations-Liste
    jeder Wert endet mit einem <br/>-Tag, und das Ganze wird in ein <li class="cards__item"> eingebettet.
    """
    output = ""
    for animal in data:
        output += '<li class="cards__item">'
        if 'name' in animal:
            output += f"Name: {animal['name']}<br/>\n"
        if 'characteristics' in animal:
            if 'diet' in animal['characteristics']:
                output += f"Diet: {animal['characteristics']['diet']}<br/>\n"
            if 'type' in animal['characteristics']:
                output += f"Type: {animal['characteristics']['type']}<br/>\n"
        if 'locations' in animal and isinstance(animal['locations'], list) and animal['locations']:
            output += f"Location: {animal['locations'][0]}<br/>\n"
        output += '</li>\n'
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
    # JSON-Daten laden
    animals_data = load_data('animals_data.json')

    # Optionale Konsolenausgabe der rohen Daten
    print_animal_info(animals_data)

    # HTML-Code für jedes Tier generieren (als "card" bzw. Listenelement)
    animals_info = generate_animals_output(animals_data)

    # Template einlesen, Platzhalter ersetzen und neue HTML-Datei erzeugen
    create_html("animals_template.html", animals_info, "animals.html")

    print("Die Datei animals.html wurde erfolgreich erstellt.")
