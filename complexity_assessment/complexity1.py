import json
import argparse

def score_complexity(info):
    
    score = 0

   
    amount_str = info.get("Amount", "")
    try:
        amount = float(amount_str.replace("$", "").replace(",", "").strip())
        if amount > 10000:
            score += 5
        elif amount > 5000:
            score += 3
        else:
            score += 1
    except ValueError:
       
        score += 2

   
    if "DateOfIncident" not in info or not info["DateOfIncident"]:
        score += 2

    

    return score

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculate complexity score for a claim")
    parser.add_argument("--input", required=True, help="Path to JSON file with extracted info")
    args = parser.parse_args()

    with open(args.input, "r") as f:
        info = json.load(f)

    score = score_complexity(info)
    print(f"Complexity Score: {score}")
