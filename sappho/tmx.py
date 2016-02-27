import xml.etree.ElementTree as ET


def tmx_file_to_tilemap_csv_string(tmx_file_path):
    tree = ET.parse(tmx_file_path)
    root = tree.getroot()  # <map ...>

    csv_layers = []

    for layer_data in root.findall(".//layer/data"):
        data_encoding = layer_data.attrib['encoding']

        if data_encoding != 'csv':

            raise TMXLayersNotCSV(data_encoding)

        layer_csv = layer_data.text.strip()
        csv_layers.append(layer_csv)

    return csv_layers[0]  # for now.......
