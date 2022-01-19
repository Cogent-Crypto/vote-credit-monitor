import subprocess
import time

import argparse


parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--testnet',  action='store_true')
parser.add_argument('--interval',  action='store', default=60, type=int)
args = parser.parse_args()

CONFIG = "mainnet.yml"
if args.testnet:
    CONFIG = "testnet.yml"
    DATA_DIR = "testnet_data"






def download_and_save_validator_data():
    bashCommand = f"solana validators --config {CONFIG}"
    print("running",bashCommand)
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    with open(f"{DATA_DIR}/{round(time.time())}.txt", "w") as f:
        text=output.decode("utf-8")
        text=text[text.find("\n")+1:text.find("\n  Identity ")]
        f.write(text)

while True:
    download_and_save_validator_data()
    time.sleep(60)


