import json

from openai_client import client

def perturb(positive_qualities, negative_qualities, description):

    perturbation_prompt = f"""
    You are a creative and innovative technologist that is writing descriptions of artworks for a supercomputer to generate.

    You are going to recieve a `description` of an artwork, along with `positive_qualities` for artworks and `negative_qualities` for artworks.

    You should be as loyal to these `positive_qualities` and `negative_qualities` as possible, and you should be as creative as possible in your descriptions.

    Take the `description` and write new descriptions based upon it, but with the `positive_qualities` and `negative_qualities` in mind.

    Try to be loyal to the general subject matter, main characters and style of the original `description`.

    Description: {description}

    Positive Qualities: {positive_qualities}

    Negative Qualities: {negative_qualities}

    Return your response in JSON following this schema:

    {{
      "$schema": "http://json-schema.org/draft-07/schema#",
      "title": "Artwork Description Response",
      "description": "A schema for validating the new description of an artwork, incorporating positive and negative qualities without including them explicitly in the response.",
      "type": "object",
      "properties": {{
        "new_description": {{
          "type": "string",
          "description": "A new description of the artwork that creatively incorporates the suggested positive and negative qualities."
        }}
      }},
      "required": ["new_description"]
    }}

    Here is an example of a valid response:

    {{
      "new_description": "In a vibrant tapestry of colors, the artwork unfolds a futuristic cityscape where harmony and chaos intertwine. Skyscrapers, bathed in the golden hues of sunset, reach towards a sky streaked with the last light of day, embodying the relentless pursuit of progress. Below, the city's inhabitants move in a fluid dance of daily life, their shadows elongating in the fading light. Amidst this scene, a solitary figure stands on a bridge, gazing into the horizon, symbolizing hope and contemplation in the face of overwhelming progress. This piece masterfully juxtaposes the beauty of human innovation with the solitude it can bring, inviting the viewer to reflect on the balance between advancement and the human condition."
    }}
    """

    response = client.chat.completions.create(
      model="gpt-4-turbo-preview",
      response_format= { "type": "json_object" },
      messages=[
        {"role": "user", "content": perturbation_prompt}
      ]
    )

    response_content = response.choices[0].message.content
    response_json = json.loads(response_content)

    return response_json["new_description"]

if __name__ == "__main__":
    positive_qualities = "vibrancy, innovation, hope"
    negative_qualities = "solitude, chaos"
    description = "A cityscape at dusk, with the fading light casting long shadows. The busy streets hint at the energy and complexity of urban life."

    response = perturbation(positive_qualities, negative_qualities, description)
    print("Function response:", response)

