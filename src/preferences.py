import random
from dataclasses import dataclass
from time import sleep

from generate_images import generate_image, ImageResult
from perturbation import perturb
from judgment import judge, critique

@dataclass
class ImageResultSuccess:
    success : bool
    image_result : ImageResult

class UserPreferences:
    def __init__(self, db, persona):
        self.db = db
        self.persona = persona
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
            positives, negatives = critique([f"liked_artwork:{irs.success}, artwork:{irs.image_result.image}" for irs in irs_batch])
            for positive in positives:
                self.db.insert_positive_quality(positive)
            for negative in negatives:
                self.db.insert_negative_quality(negative)
            sleep(15)

        self.ready.clear()

    def print_waiting_images(self):
        for uuid, image_result in self.waiting.items():
            print(f"Image {uuid}: {image_result.path}")

    def has_waiting_images(self):
        return len(self.waiting) > 0

    def has_ready_images(self):
        return len(self.ready) > 0

    def process_waiting_images(self):
        # Iterate over all waiting images
        waiting_uuids = list(self.waiting.keys())
        for uuid in waiting_uuids:
            # Randomly decide success or failure
            success = judge(self.persona, self.waiting[uuid])
            # Judge and move the image to ready
            self.judge_image(uuid, success)
        
        # Now commit all ready images to the database
        self.commit_ready_images()

