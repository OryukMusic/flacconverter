import os
import subprocess

# def check_requirements(requirements):
#     installed_libraries = subprocess.check_output(['pip', 'list']).decode('utf-8').split('\n')
#     installed_libraries = [lib.split()[0] for lib in installed_libraries[2:-1]]
    
#     missing_libraries = [req for req in requirements if req not in installed_libraries]
    
#     if not missing_libraries:
#         print("All requirements are already installed.")
#     else:
#         print("The following requirements are missing and will be installed:", missing_libraries)
#         install_requirements('requirements.txt', missing_libraries)

# def install_requirements(requirements_file, requirements=None):
#     try:
#         if not requirements:
#             with open(requirements_file, 'r') as file:
#                 requirements = file.read().splitlines()
        
#         subprocess.run(["pip", "install"] + requirements)
#         print("All requirements installed successfully!")
#     except FileNotFoundError:
#         print(f"Error: {requirements_file} not found.")

# # Call the function with the path to your requirements.txt file
# requirements_file = 'requirements.txt'
# with open(requirements_file, 'r') as file:
#     requirements = file.read().splitlines()


# check_requirements(requirements)


from pydub import AudioSegment
import music_tag


def flac_to_mp3(input_file, output_file, bitrate='320k'):
    # Load the FLAC file
    sound = AudioSegment.from_file(input_file, format="flac")
    
    # Export the audio to MP3 format
    sound.export(output_file, format="mp3", bitrate=bitrate)

def flac_to_wav(input_file, output_file):
    #load the FLAC file
    sound = AudioSegment.from_file(input_file, format="flac")
    
    # Export the audio to MP3 format
    sound.export(output_file, format="wav")

def convert_folderWAV(input_folder, output_folder):
    for file in os.listdir(input_folder):
        if file.endswith(".flac"):
            output_file = os.path.join(output_folder, os.path.splitext(file)[0] + ".wav")
            flac_to_wav(os.path.join(input_folder, file), output_file)
            print(f"Converted: {file} to {output_file}")

def convert_folderMP3(input_folder, output_folder):
    # Iterate over each file in the input folder
    for file in os.listdir(input_folder):
        if file.endswith(".flac"):
            # Create output file path
            output_file = os.path.join(output_folder, os.path.splitext(file)[0] + ".mp3")
            # Convert FLAC to MP3
            flac_to_mp3(os.path.join(input_folder, file), output_file)
            print(f"Converted: {file} to {output_file}")

def getFileList(folder):
    files = []
    for filename in os.listdir(folder):
        f = os.path.join(folder, filename)
        if os.path.isfile(f) and (filename.endswith(".mp3") or filename.endswith(".wav")):
            files.append(f)
    return files

def getInputFileList(folder):
    files = []
    for filename in os.listdir(folder):
        f = os.path.join(folder, filename)
        if os.path.isfile(f) and filename.endswith(".flac"):
            files.append(f)
    return files

def writeMetaDataandChangeFileName(fileList, format):
    match format:
        case "1":
            for song in fileList:
                #tag = EasyID3(song)
                if song.endswith(".mp3"):
                    tag = music_tag.load_file(song)
                    title = os.path.basename(song)
                    splittedTitle = title.split(' - ')
                    tag['artist'] = splittedTitle[1]
                    tag.save()
                    if formatting == "1":
                        newName = song.replace(title, splittedTitle[2])
                    elif formatting == "2":
                        newName = song.replace(title, splittedTitle[1] + " - " + splittedTitle[2])
                    os.rename(song, newName)

                elif song.endswith(".wav"):
                    title = os.path.basename(song)
                    splittedTitle = title.split (' - ')
                    newName = song.replace(title, splittedTitle[1] + " - " + splittedTitle[2])
                    os.rename(song, newName)
        case "2":
            for song in fileList:
                #tag = EasyID3(song)
                if song.endswith(".mp3"):
                    tag = music_tag.load_file(song)
                    title = os.path.basename(song)
                    splittedTitle = title.split(' - ')
                    tag['artist'] = splittedTitle[0]
                    tag.save()
                    if formatting == "1":
                        newName = song.replace(title, splittedTitle[1])
                        os.rename(song, newName)
                    
        case "3":
            return
        
if __name__ == '__main__':  
    running = True            
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Hi and welcome to the super duper cool flac to mp3 or wav converter made by Young Ho Braakman. \n")

    while running:
        print("First, what is the format of the title of our files? \n")
        formatAsk = True
        while formatAsk:
            format = input("""
For NUMBER - ARTIST - TRACK TITLE.flac press 1\n
For ARTIST - TRACK TITLE.flac press 2 (Only makes sense for MP3)\n
For UNSUPPORTED FORMAT press 3 \n\n
                           
If your title format is unsuspported, the files won't be renamed and metadata won't be 
written into the files. \n
Metadata can only be written for MP3 files, it does NOT work for wavs.\n
Also do make sure the segments are seperated by a " - " (with spaces on both sides)\n
""")

            if format == "1" or format == "2" or format == "3":
                formatAsk = False
            else: 
                print("Please make sure you type a 1 2 or 3\n")

        print("If you are converting to MP3s, what format do you want your title to be in?\n")
        formattingAsk = True
        while formattingAsk:
            formatting = input("""
For TRACK TITLE (Artistname in Metadata) press 1\n
For ARTIST = TRACK TITLE (Artistname in Metadata) press 2\n
If you are converting to WAV press 3 \n
""")

            if formatting == "1" or formatting == "2" or formatting == "3":
                formattingAsk = False
            else: 
                print("Please make sure you type a 1 2 or 3\n")

        folderAsking = True
        while folderAsking:
            input_folder = input("Copy the path where your flacs are located\n")
            output_folder = input("Copy the path where your converted files should be saved\n")
            if input_folder == output_folder:
                print("Your output and input cannot be the same folder\n")
            else:
                try:
                    outputList = getFileList(output_folder)
                except FileNotFoundError:
                    print("Please make sure the output folder exists")

                try:
                    inputList = getInputFileList(input_folder)
                except FileNotFoundError:
                    print("Please make sure the input folder exists")

                try:
                    if len(outputList) >0:
                        print("Please make sure your output folder does not contain any wavs or mp3s")
                    elif len(inputList) == 0:
                        print("Please make sure your input folder is not empty")
                    else:
                        folderAsking = False
                except NameError:
                    pass

        asking = True
        while asking:
            mp3orwav = input("Do you want to convert to WAV or MP3? type 'W' for Wav and 'M' for MP3\n")
            if mp3orwav == 'W':
                asking = False
                convert_folderWAV(input_folder=input_folder, output_folder=output_folder)
                list = getFileList(output_folder)
                writeMetaDataandChangeFileName(list, format)
            elif mp3orwav == 'M':
                asking = False
                convert_folderMP3(input_folder=input_folder, output_folder=output_folder)
                list = getFileList(output_folder)
                writeMetaDataandChangeFileName(list, format)
            else:
                print("Please select W or M\n")

        runAsking = True

        while runAsking:
            runAsk = input("Do you want to convert more files? Y/N \n")
            if runAsk == "N":
                running = False
                runAsking = False
                print("Have fun with your converted files!")
            elif runAsk == "Y":
                runAsking = False
                print("Program reloading...")
            else:
                print("Please input Y or N\n")
        

