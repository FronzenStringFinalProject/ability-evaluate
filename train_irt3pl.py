from pathlib import Path
from sys import stderr

import torch

import dataset_loader
import result_serialize

model_type = '3pl'
# FIXME: :"nvrtc: error: failed to open nvrtc-builtins64_118.dll.
device = 'cuda' if torch.cuda.is_available() else 'cpu'

from py_irt.config import IrtConfig
from py_irt.training import IrtModelTrainer

if __name__ == '__main__':
    parsed_config = {
        "model_type": model_type,
        "epochs": 3600,
        "dropout": 0.1,
        "hidden": 150,
        "deterministic": False,
        "log_every": 100
    }

    config = IrtConfig(**parsed_config)

    # dataset = ipc_process.load_dataset_from_stdin()
    dataset = dataset_loader.load_dataset_from_stdin()
    model = IrtModelTrainer(data_path=Path("./"), config=config, dataset=dataset)

    model.train(device="cpu")

    for output in result_serialize.serialize(result_serialize.BestParams(**model.best_params)):
        stderr.write(f"{output.json()}\n")
        print(output)

    print("ending")