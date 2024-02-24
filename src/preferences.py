# preference class

# initialize with a sqlite3 database

# has a function that fetches a random prompt from the database
# fetch a prompt from the database using fetch_random_prompt
# perturb the prompt 4 times using perturb, this generates 4 new prompts
# generate 4 images using generate_image
# each generated image returns an ImageResult
# these image results should be stored in a "waiting" dictionariy variable on the object, where the key is the uuid and the value is the ImageResult
# there should also be a ready dictionary that will use the uuid as a key and store the success of the image and the ImageResult (make a class for this)

# has function that accepts an image uuid along success=True or success=False
# checks if the image is in the "waiting" variable
# if it is not, returns an error
# otherwise
# updates the database with the image uuid and the prompt using the insert_image function
# updates the database with the prompt and success fields using the insert_prompt function
# removes the image from the "waiting" variable
# adds the image to the "ready" variable along with its success

# has a function that commits the ready images
# it iterates over each of the ready images in groups of 4 (or if fewer all of them)
# it passes the success of image / ImageResult class to the judge function
# it recieves positive and negative qualities form the judge function as a tuple with 2 elements
# it updates the database with the positive and negative qualities using the insert_positive_quality and insert_negative_quality functions
# it then clears the ready variable

import random
from dataclasses import dataclass

from generate_images import generate_image, ImageResult
from perturbation import perturb
from judgment import judge

@dataclass
class ImageResultSuccess:
    success : bool
    image_result : ImageResult

class UserPreferences:
    def __init__(self, db):
        self.db = db
        self.waiting = {}  # Maps uuid to ImageResult
        self.ready = {}  # Maps uuid to ImageResultSuccess

    def fetch_and_process_prompt(self, count=4):
        prompt = self.db.fetch_random_prompt()
        positive_qualities, negative_qualities = self.db.fetch_random_qualities()
        perturbed_prompts = [perturb(positive_qualities, negative_qualities, prompt) for _ in range(count)]

        for pp in perturbed_prompts:
            img_result = generate_image(pp)
            self.waiting[img_result.uuid] = img_result

    def judge_image(self, image_uuid, success):
        if image_uuid not in self.waiting:
            return "Error: Image not found in waiting queue."

        image_result = self.waiting.pop(image_uuid)
        self.db.insert_image(image_result.uuid, image_result.prompt)
        self.db.insert_prompt(image_result.prompt, success)
        self.ready[image_uuid] = ImageResultSuccess(success, image_result)

    def commit_ready_images(self, batch_size=1):
        ready_images = [irs for uuid, irs in self.ready.items()]
        for i in range(0, len(ready_images), batch_size):
            irs_batch = ready_images[i:i+batch_size]
            print(len(irs_batch))
            positives, negatives = judge(irs_batch)
            for positive in positives:
                self.db.insert_positive_quality(positive)
            for negative in negatives:
                self.db.insert_negative_quality(negative)
            sleep(120)

        self.ready.clear()

    def has_waiting_images(self):
        return len(self.waiting) > 0

    def has_ready_images(self):
        return len(self.ready) > 0

    def process_waiting_images(self):
        # Iterate over all waiting images
        waiting_uuids = list(self.waiting.keys())
        for uuid in waiting_uuids:
            # Randomly decide success or failure
            success = random.choice([True, False])
            # Judge and move the image to ready
            self.judge_image(uuid, success)
        
        # Now commit all ready images to the database
        self.commit_ready_images()

