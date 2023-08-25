from transformers import pipeline
from diffusers import DiffusionPipeline
from PIL import ImageDraw, ImageFont
import os
import imageio
import re
import random


class DreamViewer:

    def __init__(self, config):
        self.config = config
        self.audio_text_converter = pipeline(model = config.speech_to_text)
        self.image_generator = DiffusionPipeline.from_pretrained(config.text_to_image)
        #self.image_generator = DiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5")
        self.image_generator.to("cuda")
        self.text_generator = pipeline('text-generation', model = config.text_generator)
        self.output_filename = os.path.join(config.output_dir, config.story_name + ".mp4")
        self.fps = config.fps
        self.text_cont = False
    
    def get_text(self):
        return self.audio_text_converter(self.config.audio_file)['text']

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
            self.text_cont = True
            pattern = r'\s*([Cc]ountinue\s+the\s+story\s*\.)$'
            cleaned_string = re.sub(pattern, '', audio_text)
            expanded_dreams = self.generate_text(cleaned_string)
            dreams = [s.strip() for s in expanded_dreams.replace('\n', '').replace("\'", "").split(". ")]

        # Generate and image for each sentence
        generated_images = []
        for d in dreams:
            d_image = self.get_image(d)

            # Write subtitles
            draw = ImageDraw.Draw(d_image)
            font_size = 40
            font = ImageFont.truetype('./utils/fonts/OpenSans-Semibold.ttf', size = font_size)
            text_width, text_height = draw.textsize(d, font=font)
            text_x = (d_image.size[0] - text_width) // 2
            text_y = d_image.size[1] - text_height - 10
            text_color = (255, 255, 255)
            draw.text((text_x, text_y), d, font=font, fill=text_color)

            generated_images.append(d_image)
        
        # Replicate images for desired duration
        extended_images = []
        for image in generated_images:
          for _ in range(int(3 * self.fps)):
            extended_images.append(image)

        # Save video
        imageio.mimsave(self.output_filename, extended_images, fps = self.fps)

        # Return text completion if the user asked us to complete the story
        return cleaned_string if self.text_cont else None



