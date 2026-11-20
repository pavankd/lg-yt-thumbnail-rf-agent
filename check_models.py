from thumbnail_agent.config import get_image_client

client = get_image_client()

models = client.models.list()

for model in models.data:
    if "image" in model.id.lower():
        print(model.id)