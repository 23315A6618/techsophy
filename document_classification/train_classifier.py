import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
import joblib
import argparse
def train(data_path, model_path):
    df = pd.read_csv(data_path)
    X = df['text']
    y = df['label']
    vect = TfidfVectorizer(max_features=5000)
    X_vect = vect.fit_transform(X)
    clf = RandomForestClassifier(random_state=42)
    clf.fit(X_vect, y)
    joblib.dump((vect, clf), model_path)
    print(f"Model saved to {model_path}")
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train a claim complexity classifier")
    parser.add_argument("--data", required=True, help="CSV file with columns 'text' and 'label'")
    parser.add_argument("--model", required=True, help="Path to save the trained model (joblib)")
    args = parser.parse_args()

    train(args.data, args.model)
