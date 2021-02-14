import os
from zipfile import ZipFile


def load(zip_file, destination_dir):
    delete_previous_sample(destination_dir)  # Delete the images for the previous sample
    unzip_current_sample(zip_file, destination_dir)  # Unzip and save the images for the current ZIP file
    os.remove(zip_file)  # Remove the downloaded ZIP file


def delete_previous_sample(destination_dir):
    file_list = [f for f in os.listdir(destination_dir)]
    for f in file_list:
        os.remove(os.path.join(destination_dir, f))


def unzip_current_sample(zip_file, destination_dir):
    # Unzip all the contents into the destination directory
    with ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(destination_dir)
    # Clean the directory from unwanted files
    file_list = [f for f in os.listdir(destination_dir)]
    for f in file_list:
        if not f.endswith(".png"):
            os.remove(os.path.join(destination_dir, f))


if __name__ == "__main__":
    load("D20201211T213045_IFCB109.zip", "../production")
