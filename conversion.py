import json
import xml.etree.ElementTree as ET

def json_to_xmi(json_data, root_tag="XMI", namespace="http://www.omg.org/XMI"):
    # Create the root element with the XMI namespace
    root = ET.Element(root_tag, xmlns=namespace)

    # Recursive function to convert JSON to XML
    def build_xml(parent, data):
        if isinstance(data, dict):
            for key, value in data.items():
                child = ET.SubElement(parent, key)
                build_xml(child, value)
        elif isinstance(data, list):
            for item in data:
                item_tag = "Item"  # Default tag for list items
                child = ET.SubElement(parent, item_tag)
                build_xml(child, item)
        elif data is None:
            # Replace null values with a default value (e.g., empty string)
            parent.text = ""
        else:
            parent.text = str(data)

    # Build the XML structure
    build_xml(root, json_data)

    return root

def save_xmi_file(root, output_file):
    tree = ET.ElementTree(root)
    tree.write(output_file, encoding="utf-8", xml_declaration=True)

# Example usage
if __name__ == "__main__":
    input_json_file = "testing.json"
    output_xmi_file = "output.xmi"

    # Load JSON data
    with open(input_json_file, "r") as f:
        json_data = json.load(f)

    # Convert JSON to XMI
    xmi_root = json_to_xmi(json_data)

    # Save the XMI file
    save_xmi_file(xmi_root, output_xmi_file)
    print(f"XMI file saved to {output_xmi_file}")
