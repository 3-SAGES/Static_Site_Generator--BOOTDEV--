import os 
import shutil

def copy_files_rec(source_path: str, destination_path: str) -> None:
    for entry in os.listdir(source_path):
        new_source_path = os.path.join(source_path, entry)

        if os.path.isfile(new_source_path):
            shutil.copy(new_source_path, destination_path)
            
        else:
            new_destination_path = os.path.join(destination_path, entry)
            os.mkdir(new_destination_path)
            copy_files_rec(new_source_path, new_destination_path)