"""
Quick test to verify Gemini API is working
"""
import google.generativeai as genai

# Your API key
API_KEY = "AIzaSyBt-k8WBNysaok0loP3brx_HkVpiYLZoGU"

print("Testing Gemini API...\n")

# Configure
genai.configure(api_key=API_KEY)

# List available models
print("Available models:")
for model in genai.list_models():
    if 'generateContent' in model.supported_generation_methods:
        print(f"  - {model.name}")

print("\nTrying to use gemini-1.5-flash...\n")

try:
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content("Say 'Hello, API is working!' in one sentence.")
    print(f"✅ SUCCESS! Response: {response.text}")
except Exception as e:
    print(f"❌ FAILED with gemini-1.5-flash: {e}\n")
    
    print("Trying gemini-pro instead...\n")
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content("Say 'Hello, API is working!' in one sentence.")
        print(f"✅ SUCCESS! Response: {response.text}")
        print("\n⚠️ Use 'gemini-pro' instead of 'gemini-1.5-flash' in your script")
    except Exception as e2:
        print(f"❌ FAILED with gemini-pro too: {e2}")
