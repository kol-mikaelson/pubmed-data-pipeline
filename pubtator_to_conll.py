import os
import re

def pubtator_to_conll(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        if filename.endswith(".txt"):
            input_file = os.path.join(input_dir, filename)
            output_file = os.path.join(output_dir, filename.replace(".txt", ".conll"))

            # Read PubTator data from the input file
            with open(input_file, "r") as f:
                pubtator_text = f.read()

            lines = pubtator_text.strip().split("\n")

            # Ignore the last 3 lines
            lines = lines[:-3]

            # Extract the paragraph text
            paragraph = ""
            for line in lines:
                if "|a|" in line:
                    paragraph = line.split("|a|")[1]
                    break

            # Replace "/" with a space in the paragraph
            paragraph = paragraph.replace("/", " ")

            # Extract annotations (focus on Column 4 and Column 5 for 6-column lines)
            annotations = []
            for line in lines:
                parts = line.split("\t")
                if len(parts) == 6:  
                    entity_text = parts[3].replace("/", " ")  # Replace "/" with a space in the entity text
                    entity_type = parts[4]
                    annotations.append((entity_text, entity_type))

            # Tokenize the paragraph and initialize tags
            tokens = paragraph.split()
            tags = ["O"] * len(tokens)

            # Normalize tokens
            normalized_tokens = [re.sub(r'[^\w]', '', token).lower() for token in tokens]

            for entity_text, entity_type in annotations:
                entity_tokens = entity_text.split()
                normalized_entity_tokens = [re.sub(r'[^\w]', '', token).lower() for token in entity_tokens]

                for i in range(len(normalized_tokens) - len(normalized_entity_tokens) + 1):
                    if normalized_tokens[i:i + len(normalized_entity_tokens)] == normalized_entity_tokens:
                        tags[i] = f"B-{entity_type}"
                        for j in range(1, len(normalized_entity_tokens)):
                            tags[i + j] = f"I-{entity_type}"

            # Format the output in CoNLL format
            conll_lines = []
            for token, tag in zip(tokens, tags):
                conll_lines.append(f"{token} {tag}")
                if token in ".!?":  
                    conll_lines.append("")

            conll_output = "\n".join(conll_lines)

            # Save the CoNLL output to the output file
            with open(output_file, "w") as f:
                f.write(conll_output)

            print(f"CoNLL format saved to {output_file}")

if __name__ == "__main__":
    input_dir = "data/pubmed_responses"  
    output_dir = "data/conll_out"
    pubtator_to_conll(input_dir, output_dir)
