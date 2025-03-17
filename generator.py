import requests
from PIL import Image
from io import BytesIO
import json

def generator(prompt=None, save_path="./", authorization_token=None):
    if authorization_token is None:
        print("Error: Authorization token is required")
        return False
    
    if prompt is None or len(prompt) < 5:
        print("Error: Prompt must be at least 5 characters long")
        return False
    
    API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1"
    
    try:
        response = requests.post(
            API_URL,
            headers={"Authorization": f"Bearer {authorization_token}"},
            json={"inputs": str(prompt)}
        )
        
        # Check the response status code
        if response.status_code == 200:
            try:
                # Try to open the image
                i = Image.open(BytesIO(response.content))
                i.save(f"{save_path}image.png")
                print("Image successfully generated and saved!")
                return True
            except Exception as e:
                print(f"Error: Could not process the response as an image: {str(e)}")
                try:
                    # Try to decode the response content as JSON to see if it's an error message
                    error_content = json.loads(response.content)
                    print(f"API Response content: {error_content}")
                except:
                    # If it's not JSON, print the raw content
                    print(f"API Response content: {response.content[:500]}...")
                return False
        elif response.status_code == 401:
            print("Error: Invalid authorization token or unauthorized access")
            print(f"Response content: {response.content.decode('utf-8', errors='ignore')}")
            return False
        elif response.status_code == 503:
            print("Error: Model is currently loading or the service is unavailable")
            print(f"Response content: {response.content.decode('utf-8', errors='ignore')}")
            return False
        else:
            print(f"Error: Unexpected status code {response.status_code}")
            print(f"Response content: {response.content.decode('utf-8', errors='ignore')}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"Error making request to the API: {str(e)}")
        return False

if __name__=="__main__":
    generator(prompt="Sheep with violin", authorization_token="<Your_token>")
