from config import GenerationArgsDefault, DreamViewerConfig
from DreamViewer import DreamViewer
from argparse import ArgumentParser
from utils import set_seed
import os

def get_args():
    parser = ArgumentParser()
    parser.add_argument(
        "--audio_file",
        type = str,
        default = GenerationArgsDefault.INIT_AUDIO_FILE,
        help = f"Audio file that contains the story we want to visualize. Default: {GenerationArgsDefault.INIT_AUDIO_FILE}"
    )
    parser.add_argument(
        "--story_name",
        type = str,
        default = GenerationArgsDefault.STORY_NAME,
        help = f"Name of the story to generate. Default: {GenerationArgsDefault.STORY_NAME}"
    )
    parser.add_argument(
        "--output_dir",
        type = str,
        default = GenerationArgsDefault.OUTPUT_DIR,
        help = f"Ouput directory where the media will be stored. Default: {GenerationArgsDefault.OUTPUT_DIR}"
    )
    parser.add_argument(
        "--seed",
        type = int,
        default = GenerationArgsDefault.SEED,
        help = f"Seed to be used. Default: {GenerationArgsDefault.SEED}"
    )

    return parser.parse_args()

def main():
    args = get_args()
    set_seed(args.seed)
    config = DreamViewerConfig(**{k:v for k,v in vars(args).items()})
    os.makedirs(args.output_dir, exist_ok=True)
    dv = DreamViewer(config)
    dv.generate()




if __name__ == "__main__":
    main()