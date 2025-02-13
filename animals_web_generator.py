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
    Generiert einen HTML-formatierten String, in dem für jedes Tier ein Listenelement
    erzeugt wird, das wie folgt strukturiert ist:

    <li class="cards__item">
      <div class="card__title">{Name}</div>
      <p class="card__text">
          <strong>Diet:</strong> {Diet}<br/>
          <strong>Location:</strong> {Location}<br/>
          <strong>Type:</strong> {Type}<br/>
      </p>
    </li>
    """
    output = ""
    for animal in data:
        output += '<li class="cards__item">\n'
        # Name als Titel
        if 'name' in animal:
            output += f'  <div class="card__title">{animal["name"]}</div>\n'
        # Beginne den Text-Block
        output += '  <p class="card__text">\n'
        # Diet aus characteristics
        if 'characteristics' in animal and 'diet' in animal['characteristics']:
            output += f'      <strong>Diet:</strong> {animal["characteristics"]["diet"]}<br/>\n'
        # Location (erster Eintrag)
        if 'locations' in animal and isinstance(animal['locations'], list) and animal['locations']:
            output += f'      <strong>Location:</strong> {animal["locations"][0]}<br/>\n'
        # Type aus characteristics
        if 'characteristics' in animal and 'type' in animal['characteristics']:
            output += f'      <strong>Type:</strong> {animal["characteristics"]["type"]}<br/>\n'
        # Text-Block beenden
        output += '  </p>\n'
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

    # Optional: Rohdaten in der Konsole ausgeben
    print_animal_info(animals_data)

    # HTML-Code für jedes Tier generieren (als "card")
    animals_info = generate_animals_output(animals_data)

    # Template einlesen, Platzhalter ersetzen und neue HTML-Datei erzeugen
    create_html("animals_template.html", animals_info, "animals.html")

    print("Die Datei animals.html wurde erfolgreich erstellt.")
