import json


def load_data(file_path):
    """Lädt eine JSON-Datei."""
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


def serialize_animal(animal_obj):
    """
    Serialisiert ein einzelnes Tier-Objekt in ein HTML-Listenelement.
    Das Format entspricht:

    <li class="cards__item">
      <div class="card__title">{Name}</div>
      <p class="card__text">
          <strong>Diet:</strong> {Diet}<br/>
          <strong>Location:</strong> {Location}<br/>
          <strong>Type:</strong> {Type}<br/>
      </p>
    </li>
    """
    output = ''
    output += '<li class="cards__item">\n'
    if 'name' in animal_obj:
        output += f'  <div class="card__title">{animal_obj["name"]}</div>\n'
    output += '  <p class="card__text">\n'
    if 'characteristics' in animal_obj and 'diet' in animal_obj['characteristics']:
        output += f'      <strong>Diet:</strong> {animal_obj["characteristics"]["diet"]}<br/>\n'
    if 'locations' in animal_obj and isinstance(animal_obj['locations'], list) and animal_obj['locations']:
        output += f'      <strong>Location:</strong> {animal_obj["locations"][0]}<br/>\n'
    if 'characteristics' in animal_obj and 'type' in animal_obj['characteristics']:
        output += f'      <strong>Type:</strong> {animal_obj["characteristics"]["type"]}<br/>\n'
    output += '  </p>\n'
    output += '</li>\n'
    return output


def generate_animals_output(data):
    """
    Generiert einen HTML-formatierten String, indem für jedes Tier die Funktion
    serialize_animal() aufgerufen wird.
    """
    output = ''
    for animal in data:
        output += serialize_animal(animal)
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

    # Optionale Ausgabe der rohen Daten in der Konsole
    print_animal_info(animals_data)

    # HTML-Code für jedes Tier generieren
    animals_info = generate_animals_output(animals_data)

    # Template einlesen, Platzhalter ersetzen und neue HTML-Datei erzeugen
    create_html("animals_template.html", animals_info, "animals.html")

    print("Die Datei animals.html wurde erfolgreich erstellt.")
