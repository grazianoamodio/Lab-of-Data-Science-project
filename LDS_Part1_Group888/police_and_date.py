import csv
import xml.etree.ElementTree as ET

# Leggiamo il file xml e creiamo un dizionario per il merge con il file "police.csv"
def parse_xml(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    data_dict = {}

    for row in root.findall('.//row'):
        date = row.find('date').text
        date_pk = int(row.find('date_pk').text)

        data_dict[date_pk] = {'date': date, 'date_pk': date_pk}

    print("Dizionario XML creato:")
    for key, value in data_dict.items():
        print(f"{key}: {value}")

    return data_dict

# Andiamo a indicare i percorsi dei file da leggere e scrivere
xml_file_path = '/Volumes/Graziano Amodio/Data science - esami /LDS/LDS_Project_2023/dates.xml'
xml_data = parse_xml(xml_file_path)
csv_file_path = '/Volumes/Graziano Amodio/Data science - esami /LDS/LDS_Project_2023/Police.csv'
output_file_path = '/Volumes/Graziano Amodio/Data science - esami /LDS/LDS_Project_2023/police_date.csv'

# Eseguiamo il merge dei file ON (date.date_pk = police.date_fk)
with open(csv_file_path, 'r') as csv_file, open(output_file_path, 'w', newline='') as output_file:
    csv_reader = csv.DictReader(csv_file)
    fieldnames = csv_reader.fieldnames + ['date']

    csv_writer = csv.DictWriter(output_file, fieldnames=fieldnames)
    csv_writer.writeheader()

    for row in csv_reader:
        date_fk = int(row['date_fk'])  # 'date_fk' chiave esterna

        # Merge sulla chiave primaria 'date_fk'
        if date_fk in xml_data:
            row['date'] = xml_data[date_fk]['date']

        csv_writer.writerow(row)

print(f'Merge completato. Risultati in: {output_file_path}')
