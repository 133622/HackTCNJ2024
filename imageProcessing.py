import vertexai
from vertexai.generative_models import GenerativeModel, Image

def generate_text(project_id: str, file_path: str) -> str:
    # Initialize Vertex AI
    vertexai.init(project=project_id)
    # Load the model
    model = GenerativeModel("gemini-pro-vision")

    img = Image.load_from_file(file_path)
    # print(type(img))

    # Query the model
    response = model.generate_content([
        img, "Very briefly explain the central highlight image (around 20 words). Don't include the word screenshot when describing the image. Start the description with 'This is...'."
        ])
    topic = model.generate_content([response.text, "What is the main subject of this text? (e.g. 'a cat')"])

    # print(response)
    return response.text, topic.text
    # return

# response, topic = generate_text("hacktcnj2024", "screenshots/screenshot.jpg")
# print(response, "\n",topic)