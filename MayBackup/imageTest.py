import requests
from PIL import Image
from io import BytesIO

# URL of the image
url = "https://i.scdn.co/image/ab67616100005174ee07b5820dd91d15d397e29c"

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Read the image data from the response content
    image_data = response.content

    # Open the image using PIL
    image = Image.open(BytesIO(image_data))

    # Display the image
    image.show()
else:
    print("Failed to download the image")
