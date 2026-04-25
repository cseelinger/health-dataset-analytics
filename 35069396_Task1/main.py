"""
This module should import the rest of the modules and start the application. 
The user should be able to launch your application by navigating to the file tree 
and running “python3 main.py” in the terminal.
"""
from load_dataset_module import LoadDataset
from user_interface_module import UserInterface

import logging
import os

def make_new_dir_file():
    os.makedirs('logs', exist_ok=True)

def main():
    # initialize logging
    make_new_dir_file()
    logging.basicConfig(
        filename='logs/patient_health_analytics.log',
        filemode='w',
        level=logging.INFO,
        format = '%(asctime)s %(levelname)s %(message)s',
        datefmt = '%y-%m-%d %H:%M:%S',
    )

    loader = LoadDataset("data.csv")
    data = loader.load_dataset()
    interface = UserInterface(data)
    interface.start_interface()

if __name__ == "__main__":
    main()