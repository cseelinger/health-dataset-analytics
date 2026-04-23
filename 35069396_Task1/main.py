"""
This module should import the rest of the modules and start the application. 
The user should be able to launch your application by navigating to the file tree 
and running “python3 main.py” in the terminal.
"""
from load_dataset_module import LoadDataset
from query_module import QueryModule
from user_interface_module import UserInterface

def main():
    loader = LoadDataset("data.csv")
    data = loader.load_dataset()
    queries = QueryModule(data)
    interface = UserInterface(data)
    interface.start_interface()

if __name__ == "__main__":
    main()