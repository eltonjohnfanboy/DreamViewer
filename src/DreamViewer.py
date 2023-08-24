from transformers import pipeline
from diffusers import DiffusionPipeline
from PIL import Image
import os
import imageio
import re
import random


class DreamViewer:

    def __init__(self, config):
        self.config = config
        self.audio_text_converter = pipeline(model = config.speech_to_text)
        self.audio_text_converter.to("cuda")
        self.image_generator = DiffusionPipeline.from_pretrained(config.text_to_image)
        self.image_generator = DiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5")
        self.image_generator.to("cuda")
        self.text_generator = pipeline('text-generation', model = config.text_generator)
        self.output_filename = os.join(config.output_dir, config.story_name + ".mp4")
        self.fps = config.fps
    
    def get_text(self):
        return str("Once upon a time there was a kid. Countinue the story.")
        #return self.audio_text_converter(self.config.audio_file)['text']

    def get_image(self, text):
        return self.image_generator(text).images[0]

    def generate_text(self, initial_text):
        return self.ftext_generator(initial_text, max_length = 100, num_return_sequences = 5)[random.randint(0,4)]['generated_text']

    def generate(self):

        # Get the audio text
        audio_text = self.get_text()

        # Separate audio text in different sentences
        dreams = [s.strip() for s in audio_text.split(". ")]

        # If the users asks us to countinue the story we use the text-generation model to do so
        if re.sub(r'[^\w\s]', '', dreams[-1]).lower() == 'countinue the story':
            pattern = r'\s*([Cc]ountinue\s+the\s+story\s*\.)$'
            cleaned_string = re.sub(pattern, '', audio_text)
            expanded_dreams = self.generate_text(cleaned_string)
            dreams = [s.strip() for s in expanded_dreams.replace('\n', '').replace("\'", "").split(". ")]

        # Generate and image for each sentence
        generated_images = []
        for d in dreams:
            d_image = self.get_image(d)
            generated_images.append(d_image)
        
        # Replicate images for desired duration
        extended_images = []
        for image in generated_images:
          for _ in range(int(3 * self.fps)):
            extended_images.append(image)

        # Save video
        fps = 30
        imageio.mimsave(self.output_filename, extended_images, fps = self.fps)



