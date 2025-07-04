import argparse

def route_claim(score, threshold=5):
    
    if score < threshold:
        return "auto_process"
    else:
        # Priority can be the score itself or normalized
        return f"human_review (priority={score})"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Route claim based on complexity score")
    parser.add_argument("--score", type=int, required=True, help="Complexity score")
    parser.add_argument("--threshold", type=int, default=5, help="Threshold for routing decision")
    args = parser.parse_args()

    decision = route_claim(args.score, args.threshold)
    print(f"Routing Decision: {decision}")
