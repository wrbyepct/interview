"""
Batch prediction script for MNIST digit recognition.

Processes all images in a directory and outputs predictions to CSV.
"""
import sys
import csv
import argparse
from pathlib import Path
from typing import Optional

import torch
from torchvision import transforms
from PIL import Image, UnidentifiedImageError

from app.model import CNNTransformer


def load_model(weights_path: str) -> torch.nn.Module:
    """
    Load model once and set to evaluation mode.

    Args:
        weights_path: Path to model weights file

    Returns:
        Loaded model in eval mode
    """
    model = CNNTransformer()
    model.load_state_dict(torch.load(weights_path, map_location='cpu'))
    model.eval()  # CRITICAL: Sets dropout/batchnorm to inference mode
    return model


def process_batch(model: torch.nn.Module, image_dir: Path, output_csv: Path) -> None:
    """
    Process all images in directory and write results to CSV.

    Args:
        model: Loaded PyTorch model in eval mode
        image_dir: Directory containing images to process
        output_csv: Path to output CSV file
    """
    # Define preprocessing (identical to app/main.py lines 69-72)
    transform = transforms.Compose([
        transforms.Resize((28, 28)),
        transforms.ToTensor(),
    ])

    # Open CSV for writing (stream results, don't accumulate in memory)
    fieldnames = ['filename', 'predicted_digit', 'confidence']
    with open(output_csv, 'w', newline='') as csvfile:  # newline='' for Windows compatibility
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # Iterate images (generator pattern - memory efficient)
        # Case-insensitive pattern matching for jpg, jpeg, png, JPG, JPEG, PNG
        processed_count = 0
        error_count = 0

        for img_path in sorted(image_dir.glob("*.[jpJP][npNP]*[gG]")):
            try:
                # Load and preprocess (identical to app/main.py line 66)
                img = Image.open(img_path).convert("L")  # Convert to grayscale
                img_tensor = transform(img).unsqueeze(0)  # Add batch dimension

                # Inference (identical to app/main.py lines 76-79)
                with torch.inference_mode():
                    output = model(img_tensor)
                    pred = torch.argmax(output, dim=1).item()
                    confidence = torch.softmax(output, dim=1).max().item()

                # Write result immediately
                writer.writerow({
                    'filename': img_path.name,
                    'predicted_digit': pred,
                    'confidence': confidence
                })
                processed_count += 1

            except UnidentifiedImageError:
                print(f"Warning: Could not identify image {img_path.name}, skipping")
                error_count += 1
            except Exception as e:
                print(f"Error processing {img_path.name}: {e}, skipping")
                error_count += 1

        print(f"Processed {processed_count} images successfully")
        if error_count > 0:
            print(f"Skipped {error_count} images due to errors")


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description='Batch predict digits from images using trained MNIST model'
    )
    parser.add_argument(
        '--model-path',
        default='model_weights.pth',
        help='Path to model weights file (default: model_weights.pth)'
    )
    parser.add_argument(
        '--image-dir',
        default='test',
        help='Directory containing images to process (default: test)'
    )
    parser.add_argument(
        '--output',
        default='result.csv',
        help='Output CSV file path (default: result.csv)'
    )
    return parser.parse_args()


def main():
    """Main entry point for batch prediction script."""
    args = parse_args()

    # Validate paths
    model_path = Path(args.model_path)
    if not model_path.exists():
        print(f"Error: Model file not found: {model_path}")
        sys.exit(1)

    image_dir = Path(args.image_dir)
    if not image_dir.is_dir():
        print(f"Error: Image directory not found: {image_dir}")
        sys.exit(1)

    # Load model once
    print(f"Loading model from {model_path}...")
    model = load_model(str(model_path))
    print("Model loaded successfully")

    # Process batch
    output_path = Path(args.output)
    print(f"Processing images from {image_dir}...")
    process_batch(model, image_dir, output_path)
    print(f"Results written to {output_path}")


if __name__ == "__main__":
    main()
