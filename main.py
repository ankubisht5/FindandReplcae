import zipfile
import os
import logging
import datetime

def extract_zip(zip_file_name, find_replace_pairs):
    """Extracts a zip file and replaces all occurrences of the strings in `find_replace_pairs` with the corresponding strings.

    Args:
        zip_file_name: The name of the zip file to extract.
        find_replace_pairs: A dictionary of strings, where the keys are the strings to find and the values are the strings to replace them with.

    """
    now = datetime.datetime.now()
    # Format the time as a string
    timestamp = now.strftime('%Y-%m-%d_%H-%M-%S')
    tmp_path = "/tmp/"+zip_file_name+timestamp
    # Create a ZipFile object
    try:
        with zipfile.ZipFile(zip_file_name, "r") as zip_file:
            zip_file.extractall(tmp_path)
            zip_file.close()
    except zipfile.BadZipFile as e:
        logging.error("Error extracting zip file: %s", e)
        return
    # Close the ZipFile object
    # Get the list of files in the zip file
    files = os.listdir(tmp_path)
    print("Files are: "+ str(files) + " in " + tmp_path +" directory")
    # Iterate over the files in the zip file
    for file in files:
        if file.endswith('.xml'):
        # Open the file in read mode
            with open(tmp_path+'\\'+file, "r") as f:
                # Read the contents of the file
                    contents = f.read()
                    # Replace the keywords
                    for v_find, v_replace in find_replace_pairs.items():
                        if contents.count(v_find) >1:
                            logging.debug("Replacing %s with %s in %s (%d instances)", v_find, v_replace, file, contents.count(v_find))
                        else:
                            logging.warn("Replacing %s with %s in %s (%d instances)", v_find, v_replace, file, contents.count(v_find))
                        contents = contents.replace(v_find, v_replace)
                    # Write the contents of the file to a new file
                    with open(file, "w") as f:
                        f.write(contents)
                        f.close()
        if file.endswith('.zip'):
            extract_zip(tmp_path+'\\'+file, find_replace_pairs)


def main():
    # Get the name of the zip file
    now = datetime.datetime.now()
    # Format the time as a string
    timestamp = now.strftime('%Y-%m-%d_%H-%M-%S')
    logging.basicConfig(filename='/log/my_log'+timestamp, level=logging.DEBUG)
    zip_file_name = input("Enter the zip file name:")
    # Get the list of find and replace pairs
    find_replace_pairs = {}
    while True:
        find = input("Enter the string to find:")
        if find == '':
            break
        replace = input("Enter the string to replace:")
        if replace == '':
            break
        find_replace_pairs[find] = replace
    try:
        extract_zip(zip_file_name, find_replace_pairs)
    except Exception as e:
        logging.error("Error in extract_zip function: %s", e)

if __name__ == "__main__":
    main()