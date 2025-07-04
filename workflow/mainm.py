import argparse
import os
import json
import tempfile
import pytesseract
import utils
print(utils.__file__)
print(dir(utils))


# Import your modules (adjust import paths as needed)
from utils import  pdf_to_images, preprocess_image
from document_classification.predict import predict as classify_claim
from information_extraction.extract_info import extract_key_info
from complexity_assessment.complexity_score import score_complexity
from decision_engine.routing import route_claim

def ocr_document(path):
    ext = os.path.splitext(path)[1].lower()
    texts = []

    if ext == '.pdf':
        images = pdf_to_images(path)
        processed_imgs = [preprocess_image(img) for img in images]
        for img in processed_imgs:
            text = pytesseract.image_to_string(img)
            texts.append(text)
    else:
        img = Image.open(path)
        img = preprocess_image(img)
        text = pytesseract.image_to_string(img)
        texts.append(text)

    return "\n".join(texts)

def save_json(data, filepath):
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)

def main(input_path, model_path, threshold=5):
    print(f"Processing claim document: {input_path}")

    # 1. OCR to extract text
    print("Running OCR...")
    claim_text = ocr_document(input_path)
    print("OCR completed.")

    # Save OCR text temporarily for classification and extraction
    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as temp_text_file:
        temp_text_file.write(claim_text.encode('utf-8'))
        temp_text_path = temp_text_file.name

    # 2. Classify claim complexity
    print("Classifying claim complexity...")
    import sys
    sys.path.insert(0, os.path.abspath('../02_document_classification'))
    pred_label = classify_claim(temp_text_path, model_path)
    print(f"Classification result: {pred_label}")

    # 3. Extract key info
    print("Extracting key information...")
    from information_extraction.extract_info import extract_key_info # type: ignore
    extracted_info = extract_key_info(claim_text)
    print(f"Extracted info: {extracted_info}")

    # Save extracted info to JSON
    extracted_info_path = "extracted_info.json"
    save_json(extracted_info, extracted_info_path)

    # 4. Compute complexity score
    print("Computing complexity score...")
    from complexity_assessment.complexity_score import score_complexity
    complexity_score = score_complexity(extracted_info)
    print(f"Complexity score: {complexity_score}")

    # 5. Routing decision
    print("Making routing decision...")
    from decision_engine.routing import route_claim
    decision = route_claim(complexity_score, threshold)
    print(f"Routing decision: {decision}")

    # Clean up temp file
    os.unlink(temp_text_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run full claims processing pipeline")
    parser.add_argument("--input", required=True, help="Path to claim document (pdf or image)")
    parser.add_argument("--model", required=True, help="Path to trained classifier model (.joblib)")
    parser.add_argument("--threshold", type=int, default=5, help="Complexity score threshold")
    args = parser.parse_args()

    main(args.input, args.model, args.threshold)
