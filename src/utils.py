import random
import os
import numpy as np
import torch
from argparse import ArgumentParser
from config import GenerationArgsDefault

def set_seed(seed: int):
    random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = True


def get_args_cli():
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