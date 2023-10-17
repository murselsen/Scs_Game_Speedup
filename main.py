import ctypes.wintypes
import logging
import os
import shutil
import sys
import time

CSIDL_PERSONAL = 5  # My Documents
SHGFP_TYPE_CURRENT = 0  # Get current, not default value

global result, appMainPath, buf, myDocuments, gameList, SII_exe, active_profile, active_save, profileTable, saveTable
buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
ctypes.windll.shell32.SHGetFolderPathW(None, CSIDL_PERSONAL, None, SHGFP_TYPE_CURRENT, buf)
myDocumentsPath = buf.value

profileTable = {'ID': [], 'Profile': [], 'Path': []}
gameList = {"ets": "Euro Truck Simulator 2", "ats": "American Truck Simulator"}
SII_exe = os.path.join(os.getcwd(), "_internal", "profile_decrypt.exe")


def main():
    def cwd():
        label = "📂 | Where I am:  |"
        labelLength = len(label)
        cwd = os.getcwd() + " |"
        cwdLength = len(cwd)
        print("\n+", "-".center(labelLength - 1, "-"), "+", "-".center(cwdLength - 2, "-"), "+")
        print("|", label, cwd)
        print("+", "-".center(labelLength - 1, "-"), "+", "-".center(cwdLength - 2, "-"), "+\n")

    # Use a breakpoint in the code line below to debug your script.
    if (sys.argv[1]):
        _selectGame = sys.argv[1]

        logging.basicConfig(filename=_selectGame+".log", level=logging.INFO)

        if _selectGame == '' or _selectGame == ' ':
            print(
                " Error Input : ", _selectGame
            )
            os.system('cls')
            os.execl(sys.executable, "start " + os.path.abspath(__file__))
        else:
            _selectGameResult = gameList.get(_selectGame)
            print("\nSelect Game: ", _selectGameResult)
            _selectGamePath = os.path.join(myDocumentsPath, _selectGameResult)
            print("Select Game Path :", _selectGamePath)
            _selectGamePathExists = os.path.exists(_selectGamePath)
            if _selectGamePathExists:
                _selectGameProfilesPath = os.path.join(_selectGamePath, "Profiles")
                os.chdir(_selectGameProfilesPath)
                for profile_index, profile in enumerate(os.listdir(os.getcwd())):
                    if profile == "desktop.ini":
                        continue
                    else:

                        _profile = profile
                        _profilePath = os.path.join(os.getcwd(), profile)
                        print("\n", _profile.center(int(len(_profile) + 35), "_"))
                        print(" *** ___[", profile_index, "] | Profile : ", _profile + "___ ***\n")
                        os.chdir(_profilePath)
                        _decrypt_app = "profile_decrypt.exe"
                        _Sii_Exe_Exists = os.path.exists(os.path.join(_profilePath, _decrypt_app))
                        if _Sii_Exe_Exists == False:
                            shutil.copyfile(SII_exe, os.path.join(os.getcwd(), _decrypt_app))

                        for file_index, file in enumerate(os.listdir(os.getcwd())):
                            if file == "profile.sii":
                                cmd = _decrypt_app + " " + file
                                print(
                                    " * Profile Decrypting the file that holds the information. \n Please wait....\n ")
                                time.sleep(2.5)

                                result = os.system(str(cmd))

                                print("\n * System Code : ", cmd, "\n", " * Result :", result)

                                if result:

                                    print(" * Profile SII Reading....")
                                    newLines = []
                                    with open("profile.sii", "r") as profileDetailReading:

                                        lines = profileDetailReading.readlines()
                                        for line_index, line in enumerate(lines):
                                            if line.startswith(" cached_discovery["):
                                                continue
                                            else:
                                                if line.startswith(" cached_discovery:"):
                                                    line = " cached_discovery: 0\n"
                                                else:
                                                    pass
                                            newLines.append(line)

                                    print(" * Profile SII Writing...")
                                    print(newLines)
                                    with open("profile.sii", "w") as profileDetailWriting:
                                        profileDetailWriting.writelines(newLines)

                                    print(profile," Cached Discovery truncated !\n")

                    os.chdir(_selectGameProfilesPath)

            else:
                os.system("exit")
            input("🚪 | Press any key to exit :")


    else:
        _selectGame = input("Choose the game you want to align: ")


"""
 

if _selectGame == '' or _selectGame == ' ':
    print(
        " Error Input : ", _selectGame
    )
os.system('cls')
os.execl(sys.executable, "start " + os.path.abspath(__file__))
else:
print("Input : ", _selectGame)

_selectGameResult = gameList.get(_selectGame)
print("\nSelect Game: ", _selectGameResult)
_selectGamePath = os.path.join(myDocumentsPath, _selectGameResult)
print("Select Game Path :", _selectGamePath)

_selectGamePathExists = os.path.exists(_selectGamePath)
# print("Select Game Path Exists Result :", _selectGamePathExists)

if _selectGamePathExists:
    os.chdir(_selectGamePath)
# cwd()
# Profiles Path
_selectGameProfilesPath = os.path.join(_selectGamePath, "Profiles")
# print("Select Game Profiles Path :", _selectGameProfilesPath)

_selectGameProfilePathExists = os.path.exists(_selectGameProfilesPath)
# print("Select Game Profiles Path Exists Result :", _selectGameProfilePathExists)

if _selectGameProfilePathExists:
    os.chdir(_selectGameProfilesPath)
# cwd()
print("Profile List")
print("------------------")
for profileDir_index, profileDir in enumerate(os.listdir(os.getcwd())):
    print(
        "---------------------------------------------------------------------------------------------")
print("[", profileDir_index, "] | Active Profile\n"
                             "[", profileDir_index, "] | -> Name :", profileDir)
_activeProfilePath = os.path.join(os.getcwd(), profileDir)
_activeProfilePathExists = os.path.exists(_activeProfilePath)
os.chdir(_activeProfilePath)
shutil.copyfile(SII_exe, os.getcwd() + "/SII.exe")

_activeProfileInfoFilePath = os.path.join(_activeProfilePath, "profile.sii")

_activeProfileInfoFilePathExists = os.path.exists(_activeProfileInfoFilePath)
cmd = "SII.exe profile.sii"
os.system(cmd)
# time.sleep(1.0)
# cwd()
print("Profile SII Reading....")
newLines = []
with open("profile.sii", "r") as profileDetailReading:

    lines = profileDetailReading.readlines()
for line_index, line in enumerate(lines):
    if
line.startswith(" cached_discovery["):
del lines[line_index]
else:
if line.startswith(" cached_discovery:"):
    line = " cached_discovery: 0\n"
else:
    pass
newLines.append(line)
# print(newLines)
print("Profile SII Writing...")
with open("profile.sii", "w") as profileDetailWriting:
    profileDetailWriting.writelines(newLines)

print(
    "Cached Stats AND Discovery truncated !"
)

input("🚪 | Press any key to exit :")
"""

# Press the green button in the gutter to run the script.


if __name__ == '__main__':
    print(SII_exe)
    try:
        print(" ************************************************************")
        print("*      Company: The King'S Works                             *")
        print("*      Product Name : Scs Game acceleration application      *")
        print("*      Author: MQuel                                         *")
        print("*      Github: github@murselsen                              *")
        print("*      Discord: 35mursel                                     *")
        print("*      Version: v1.0                                         *")
        print("*      License: 2023 - 2030                                  *")
        print(" ************************************************************")
        main()
    except Exception as e:
        logging.error("Error : ", e)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
