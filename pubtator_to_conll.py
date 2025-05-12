import re

def pubtator_to_conll(pubtator_text):
    lines = pubtator_text.strip().split("\n")
    
    lines = lines[:-3]
    
    paragraph = ""
    for line in lines:
        if "|a|" in line:
            paragraph = line.split("|a|")[1]
            break

    annotations = []
    for line in lines:
        parts = line.split("\t")
        if len(parts) == 6:  
            entity_text = parts[3]
            entity_type = parts[4]
            annotations.append((entity_text, entity_type))

    tokens = paragraph.split()
    tags = ["O"] * len(tokens)

    normalized_tokens = [re.sub(r'[^\w]', '', token).lower() for token in tokens]

    for entity_text, entity_type in annotations:
        entity_tokens = entity_text.split()
        normalized_entity_tokens = [re.sub(r'[^\w]', '', token).lower() for token in entity_tokens]

        for i in range(len(normalized_tokens) - len(normalized_entity_tokens) + 1):
            if normalized_tokens[i:i + len(normalized_entity_tokens)] == normalized_entity_tokens:
                tags[i] = f"B-{entity_type}"
                for j in range(1, len(normalized_entity_tokens)):
                    tags[i + j] = f"I-{entity_type}"

    conll_lines = []
    for token, tag in zip(tokens, tags):
        conll_lines.append(f"{token} {tag}")
        if token in ".!?":  
            conll_lines.append("")

    return "\n".join(conll_lines)

def main(input_file, output_file):
    # Read PubTator data from the input file
    with open(input_file, "r") as f:
        pubtator_text = f.read()

    conll_output = pubtator_to_conll(pubtator_text)

    with open(output_file, "w") as f:
        f.write(conll_output)

    print(f"CoNLL format saved to {output_file}")

if __name__ == "__main__":
    input_file = "output.txt"  
    output_file = "output_pre.conll"
    main(input_file, output_file)
