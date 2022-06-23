import os 
import time
import argparse


parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--testnet',  action='store_true')
parser.add_argument('--offset',  action='store', default=1642174577/60, type=int)

            

args = parser.parse_args()

MIN_TIME = round(time.time() - args.offset*60)
DATA_DIR = "mainnet_data"
if args.testnet:
    DATA_DIR = "testnet_data"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)



pubkey_callouts = ["DeadGodP9cErFezDuWRBQk4foLZbZfyBWmzHxGu6BLTo","Cogent51kHgGLHr7zpkpRjGYFXM57LgjHjDdqXd4ypdA", "1aine15iEqZxYySNwcHtQFt4Sgc75cbEi9wks8YgNCa", "Ninja1spj6n9t5hVYgF3PdnYz2PLnkt7rvaw3firmjs","Perf1UR2MyPK7RzTj5kBfNTDoJuhKraZ3oGt58QNwRc", "FLVgaCPvSGFguumN9ao188izB4K4rxSWzkHneQMtkwQJ", "7y5VhV4fkz6r4zUmH2UiwPjLwXzPL1PcV28or5NWkWRL", "Frog1Fks1AVN8ywFH3HTFeYojq6LQqoEPzgQFx2Kz5Ch", "JBCyKTG8h8tF7m54PELfM336i9T8Bhmeb6vLGDCCS7vZ", "PUmpKiNnSVAZ3w4KaFX6jKSjXUNHFShGkXbERo54xjb", "6TkKqq15wXjqEjNg9zqTKADwuVATR9dW3rkNnsYme1ea", "Bxmnb2F1hphsKrJhfJw1Cr1gGs5GBzxScNk9NgGNFS6f", "yYnFMMTqNEYbXvprpimzrsNc3oLHxEyhc8pgCdM1Y5C"]

def identity_credits_for_line(line):
    identity = line[2:46].strip()
    try:
        credits = int(line[141:150].strip())
    except Exception as e:
        print(e)
        print(line)
        print()
        print()
        return "0",0
    return identity, credits

def load_validator_credits(file_path):
    with open(file_path) as f:
        lines = f.readlines()
    return dict([identity_credits_for_line(line) for line in lines])
            
files = [x for x in sorted(os.listdir(DATA_DIR)) if int(x[:10]) > MIN_TIME]
def vote_credits_per_second():
    
    start_time = int(files[0][:10])
    end_time = int(files[-1][:10])
    elapsed_time = float(end_time - start_time)
    start_credits = load_validator_credits(DATA_DIR+"/"+files[0])
    end_credits = load_validator_credits(DATA_DIR+"/"+files[-1])
    vote_credits_per_second = {}
    for key, start_credits in start_credits.items():
        if key in end_credits:
            vote_credits_per_second[key] = (end_credits[key] - start_credits) / elapsed_time
    return vote_credits_per_second

def top_x_average(vote_credits, x=50):
    return sum(sorted(list(vote_credits.values()))[-x:])/x



def print_report_(vote_credits, pubkey_callouts):
    if args.testnet:
        print("testnet")
    else:
        print("mainnet")
    print(f"reporting from slot {files[0][:-4]} to slot {files[-1][:-4]}")
    print(f"cluster average: {' '*27} {top_x_average(vote_credits, x=1000)}")
    print(f"top 100 average: {' '*27} {top_x_average(vote_credits, x=100)}")
    for pubkey in pubkey_callouts:
        if pubkey in vote_credits:
            print(f"{pubkey}: {vote_credits[pubkey]}")
        # else:
            # print(f"{pubkey} not found")
            



vote_credits = vote_credits_per_second()
print_report_(vote_credits, pubkey_callouts)
