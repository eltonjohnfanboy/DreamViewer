from dataclasses import dataclass, field

@dataclass(frozen = True)
class ModelsConfig:
    SPEECH_TO_TEXT: str = "openai/whisper-small"
    #TEXT_TO_IMAGE: str = "stabilityai/stable-diffusion-2"
    #TEXT_TO_IMAGE: str = "CompVis/stable-diffusion-v1-4"
    #TEXT_TO_IMAGE: str = "stabilityai/stable-diffusion-2-1"
    #TEXT_TO_IMAGE: str = "dreamlike-art/dreamlike-photoreal-2.0"
    TEXT_TO_IMAGE: str = "prompthero/openjourney"
    TEXT_GENERATOR: str = "gpt2"
    TEXT_TO_VIDEO: str = ""
    IMG_GEN_IF_NOT_FINISHED: int =  10
    WORDS_PER_IMAGE: int = 25

@dataclass(frozen = True)
class GenerationArgsDefault:
    INIT_AUDIO_FILE: str = './test_data/test_audio1.mp3'
    STORY_NAME: str = "Sad Dad"
    OUTPUT_DIR: str = "./output_generation/Sad Dad"
    FPS: int = 30
    SEED: int =  17
    AUDIO_DATA: str = "./test_data"


@dataclass
class DreamViewerConfig:
    # model configuration
    speech_to_text: str = ModelsConfig.SPEECH_TO_TEXT
    text_to_image: str = ModelsConfig.TEXT_TO_IMAGE
    text_generator: str = ModelsConfig.TEXT_GENERATOR
    text_to_video: str = ModelsConfig.TEXT_TO_VIDEO
    img_gen_if_not_finished: int = ModelsConfig.IMG_GEN_IF_NOT_FINISHED
    words_per_image: int = ModelsConfig.WORDS_PER_IMAGE

    # generation configuration
    audio_file: str = GenerationArgsDefault.INIT_AUDIO_FILE
    story_name: str = GenerationArgsDefault.STORY_NAME
    output_dir: str = GenerationArgsDefault.OUTPUT_DIR
    fps: int = GenerationArgsDefault.FPS
    seed: int = GenerationArgsDefault.SEED




