import joblib
import argparse

def predict(text_path, model_path):
    
    with open(text_path, "r") as f:
        text = f.read()

   
    vect, clf = joblib.load(model_path)

    
    X_vect = vect.transform([text])
    pred = clf.predict(X_vect)

    print(f"Prediction: {pred[0]}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Predict claim complexity")
    parser.add_argument("--input", required=True, help="Path to text file with claim content")
    parser.add_argument("--model", required=True, help="Path to trained model (.joblib)")
    args = parser.parse_args()

    predict(args.input, args.model)
