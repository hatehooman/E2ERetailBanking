import sys
sys.path.insert(0, 'D:\\Big Data\\DS200\\E2ERetailBanking\\src')
from concurrent.futures import ThreadPoolExecutor
from cdc.cdc_handler import CDCHandler

def main():
    with open('./src/config/config_cdc.json', 'r') as f:
        config_data = json.load(f)
    
    configs = config_data['configs']

    with ThreadPoolExecutor() as executor:
        for config in configs:
            executor.submit(run_handler, config)

def run_handler(config):
    handler = CDCHandler(config)
    handler.process_changes()

if __name__ == "__main__":
    main()

