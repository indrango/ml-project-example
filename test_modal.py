"""
Test script for Modal deployment
Run after deployment to test the endpoints
"""

import requests
import base64
from pathlib import Path


def test_health(base_url: str):
    """Test the health endpoint"""
    print("\n🔍 Testing Health Endpoint...")
    response = requests.get(f"{base_url}/api/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")


def test_predict_with_url(base_url: str):
    """Test prediction with image URL"""
    print("\n🖼️  Testing Prediction with Image URL...")
    
    # Using Ultralytics test image
    image_url = "https://ultralytics.com/images/bus.jpg"
    
    # Download image and send as file
    response_download = requests.get(image_url)
    files = {'file': ('bus.jpg', response_download.content, 'image/jpeg')}
    
    response = requests.post(f"{base_url}/api/predict", files=files)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Model: {result.get('model')}")
        print(f"Detections: {result.get('num_detections')}")
        if result.get('detections'):
            print("\nFirst 3 detections:")
            for det in result.get('detections', [])[:3]:
                print(f"  - {det['class_name']}: {det['confidence']:.2f}")
    else:
        print(f"Error: {response.text}")


def test_predict_with_local_image(base_url: str, image_path: str = None):
    """Test prediction with local image file"""
    if not image_path:
        print("\n⚠️  Skipping local image test (no image provided)")
        return
        
    if not Path(image_path).exists():
        print(f"\n⚠️  Image file not found: {image_path}")
        return
    
    print(f"\n📸 Testing Prediction with Local Image: {image_path}")
    
    with open(image_path, 'rb') as f:
        files = {'file': (Path(image_path).name, f, 'image/jpeg')}
        response = requests.post(f"{base_url}/api/predict", files=files)
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Model: {result.get('model')}")
        print(f"Detections: {result.get('num_detections')}")
    else:
        print(f"Error: {response.text}")


if __name__ == "__main__":
    import sys
    
    # Get base URL from command line or use default
    if len(sys.argv) > 1:
        base_url = sys.argv[1].rstrip('/')
    else:
        print("❌ Please provide the Modal deployment URL")
        print("Usage: python test_modal.py https://<your-app>.modal.run")
        sys.exit(1)
    
    print(f"🚀 Testing Modal deployment at: {base_url}")
    print("=" * 60)
    
    # Run tests
    test_health(base_url)
    test_predict_with_url(base_url)
    
    # Test with local image if provided
    if len(sys.argv) > 2:
        test_predict_with_local_image(base_url, sys.argv[2])
    
    print("\n" + "=" * 60)
    print("✅ Tests completed!")

