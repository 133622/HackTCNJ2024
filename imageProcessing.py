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
    response = model.generate_content([img, "Explain this image. Don't include the word screenshot when describing the image."])

    return response.text
    # return

# response = generate_text("hacktcnj2024", "screenshots/screenshot.jpg")
# print(response)