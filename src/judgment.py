import json

from openai_client import client

def judge(images):

    judgment_prompt = f"""
    You are a creative and innovative technologist that is helping to discover stylistic and narrative themes that make art generated by a supercomputer better.

    You are going to receive artworks that have been generated by a supercomputer, along with whether people liked each artwork or not.

    Use the contrast between the works to determine qualties associated with the artworks that make them more or less appealing.

    If there are no artworks that people didn't like, you should just describe `positive_qualities` of the artworks.

    If there are no artworks that people liked, you should just describe `negative_qualities` of the artworks.

    Artworks: {images}

    Return your response in JSON following this schema:

    {{
      "$schema": "http://json-schema.org/draft-07/schema#",
      "type": "object",
      "properties": {{
        "positive_qualities": {{
          "type": "array",
          "items": {{
            "type": "string"
          }},
          "description": "A list of qualities associated with the artworks that make them appealing. This list can be empty if there are no positive qualities identified."
        }},
        "negative_qualities": {{
          "type": "array",
          "items": {{
            "type": "string"
          }},
          "description": "A list of qualities associated with the artworks that make them less appealing. This list can be empty if there are no negative qualities identified."
        }}
      }},
      "required": ["positive_qualities", "negative_qualities"],
      "additionalProperties": false,
      "description": "A schema defining the structure for feedback on artworks generated by a supercomputer, categorizing them into positive and negative qualities based on audience reception."
    }}

    Here is an example of a valid response:

    {{
      "positive_qualities": [
        "vibrant color usage",
        "innovative composition",
        "emotional depth",
        "Japanese motifs"
      ],
      "negative_qualities": [
        "lack of clarity in the theme",
        "overly complex for general appreciation",
        "generic looking"
      ]
    }}
    """

    response = client.chat.completions.create(
      model="gpt-4-vision-preview",
      messages=[
        {"role": "user", "content": judgment_prompt}
      ]
    )

    response_content = response.choices[0].message.content
    response_json = json.loads(response_content)

    positive_qualities, negative_qualities = response_json["positive_qualities"], response_json["negative_qualities"]

    return positive_qualities, negative_qualities

if __name__ == "__main__":
    positive_qualities = "vibrancy, innovation, hope"
    negative_qualities = "solitude, chaos"
    description = "A cityscape at dusk, with the fading light casting long shadows. The busy streets hint at the energy and complexity of urban life."

    response = perturbation(positive_qualities, negative_qualities, description)
    print("Function response:", response)

