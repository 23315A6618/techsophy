import argparse

def extract_key_info(text):
    
    info = {}

    lines = text.split('\n')
    for line in lines:
        line = line.strip()
        if line.lower().startswith("claimant:"):
            info["Claimant"] = line.split(":", 1)[1].strip()
        elif line.lower().startswith("amount:"):
            info["Amount"] = line.split(":", 1)[1].strip()
        elif line.lower().startswith("date of incident:"):
            info["DateOfIncident"] = line.split(":", 1)[1].strip()
       
    return info

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract key claim info from text")
    parser.add_argument("--input", required=True, help="Path to claim text file")
    args = parser.parse_args()

    with open(args.input, "r") as f:
        text = f.read()

    extracted_info = extract_key_info(text)
    print("Extracted Information:")
    for k, v in extracted_info.items():
        print(f"{k}: {v}")
