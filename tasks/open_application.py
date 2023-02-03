from fuzzywuzzy import fuzz
import os

def fuzzy_match(audio_note, app_dict):
    # for app_name in list(app_dict.keys()):
    #     if fuzz.token_set_ratio(audio_note, app_name)>50:
    #         return app_dict[app_name]

    app_to_open, max_ratio = '', 0

    for app_name in list(app_dict.keys()):
        if fuzz.token_sort_ratio(app_name, audio_note) > max_ratio:
            app_to_open = app_name
            max_ratio = fuzz.token_sort_ratio(app_name, audio_note)
    if max_ratio>50:
        return app_dict[app_to_open]
    else:
        return None

def scan_apps(apps_dir):
    app_dict = {}
    for path, subdir, files in os.walk(apps_dir):
        for file in files:
            if ".lnk" in file:
                app_name = file[:-4].lower()
                app_location = path.strip(".\\")+"\\"+file
                app_dict[app_name] = app_location
    return app_dict

def open_app(audio_note):
    app_dict = scan_apps("C:\ProgramData\Microsoft\Windows\Start Menu\Programs")
    # print("App_dict: \n\n\n\n\n", app_dict)
    app_location =  fuzzy_match(audio_note, app_dict)
    if app_location:
        os.startfile(app_location)
        return True
    else:
        return False
