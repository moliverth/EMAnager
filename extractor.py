import ftplib
import json
import csv
import shutil
from os.path import exists, abspath, isdir
from os import mkdir
from time import time as now

CURRENT_PATH = '/'.join(abspath(__file__).split('\\')[:-1])
DEFAULT_CSV_OUTPUT_PATH = f'{CURRENT_PATH}/CSV'

CONFIGS_FILENAME = "configs.json"
CONFIGS_LOADED = False
CREATE_CONFIGS_BKP = True
UPDATE_CONFIGS = False
LOGIN_LIMIT_TRY = 5

CONFIGS = {"LOGIN": {"ADDRESS": None,
                     "USER": None,
                     "KEY": None
                     },
           "FTP_PATH": None,
           "CSV_OUTPUT_PATH": None,
           "SAMPLE_FORM": {
               "15m": {
                   "TITLES": ["Local", "Freq", "Data", "Hora", "Temp int", "Pressao inst", "Pressao med", "Pressao max",
                              "Pressao min", "Temperatura inst", "Temperatura med", "Temperatura max",
                              "Temperatura min", "Umidade Relativa inst", "Umidade Relativa med",
                              "Umidade Relativa max", "Umidade Relativa min", "Radiação solar global inst LPPYRA02",
                              "Radiação solar global med LPPYRA02", "Radiação solar global max LPPYRA02",
                              "Radiação solar global min LPPYRA02", "Radiação solar global inst LPNET14",
                              "Radiação solar global med LPNET14", "Radiação solar global max LPNET14",
                              "Radiação solar global min LPNET14", "Radiação solar refletida inst ",
                              "Radiação solar refletida med ", "Radiação solar refletida max ",
                              "Radiação solar refletida min ", "Radiação IV inst", "Radiação IV med", "Radiação IV max",
                              "Radiação IV min", "Radiação spf inst", "Radiação spf med", "Radiação spf max",
                              "Radiação spf min", "Radiação solar líquida inst", "Radiação solar líquida med",
                              "Radiação solar líquida max", "Radiação solar líquida min",
                              "Temperatura inst LPNET14 (NTC)", "Temperatura med LPNET14 (NTC)",
                              "Temperatura max LPNET14 (NTC)", "Temperatura min LPNET14 (NTC)", "Direção vento med ",
                              "Direção vento max ", "Direção vento min ", "Velocidade vento med ",
                              "Velocidade vento max ", "Velocidade vento min ", "Temp solo inst", "Temp solo med",
                              "Temp solo max", "Temp solo min", "Umid solo inst", "Umid solo med", "Umid solo max",
                              "Umid solo min", "Precipitação"],
                   "UNITS": ["", "", "", "", "°C", "hPa", "hPa", "hPa", "hPa", "°C", "°C", "°C", "°C", "%", "%", "%",
                             "%", "W/m²", "W/m²", "W/m²", "W/m²", "W/m²", "W/m²", "W/m²", "W/m²", "W/m²", "W/m²",
                             "W/m²", "W/m²", "W/m²", "W/m²", "W/m²", "W/m²", "W/m²", "W/m²", "W/m²", "W/m²", "W/m²",
                             "W/m²", "W/m²", "W/m²", "°C", "°C", "°C", "°C", "°", "°", "°", "m/s", "m/s", "m/s", "°C",
                             "°C", "°C", "°C", "m³/m³", "m³/m³", "m³/m³", "m³/m³", "mm"]
               },
               "1h": {
                   "TITLES": ["Local", "Freq", "Data", "Hora", "Temp int", "Pressao inst", "Pressao med", "Pressao max",
                              "Pressao min", "Temperatura inst", "Temperatura med", "Temperatura max",
                              "Temperatura min", "Umidade Relativa inst", "Umidade Relativa med",
                              "Umidade Relativa max", "Umidade Relativa min", "Radiação solar global inst LPPYRA02",
                              "Radiação solar global med LPPYRA02", "Radiação solar global max LPPYRA02",
                              "Radiação solar global min LPPYRA02", "Radiação solar global inst LPNET14",
                              "Radiação solar global med LPNET14", "Radiação solar global max LPNET14",
                              "Radiação solar global min LPNET14", "Radiação solar refletida inst ",
                              "Radiação solar refletida med ", "Radiação solar refletida max ",
                              "Radiação solar refletida min ", "Radiação IV inst", "Radiação IV med", "Radiação IV max",
                              "Radiação IV min", "Radiação spf inst", "Radiação spf med", "Radiação spf max",
                              "Radiação spf min", "Radiação solar líquida inst", "Radiação solar líquida med",
                              "Radiação solar líquida max", "Radiação solar líquida min",
                              "Temperatura inst LPNET14 (NTC)", "Temperatura med LPNET14 (NTC)",
                              "Temperatura max LPNET14 (NTC)", "Temperatura min LPNET14 (NTC)", "Direção vento med ",
                              "Direção vento max ", "Direção vento min ", "Velocidade vento med ",
                              "Velocidade vento max ", "Velocidade vento min ", "Temp solo inst", "Temp solo med",
                              "Temp solo max", "Temp solo min", "Umid solo inst", "Umid solo med", "Umid solo max",
                              "Umid solo min", "Bateria", "Precipitacao"],
                   "UNITS": ["", "", "", "", "°C", "hPa", "hPa", "hPa", "hPa", "°C", "°C", "°C", "°C", "%", "%", "%",
                             "%", "W/m²", "W/m²", "W/m²", "W/m²", "W/m²", "W/m²", "W/m²", "W/m²", "W/m²", "W/m²",
                             "W/m²", "W/m²", "W/m²", "W/m²", "W/m²", "W/m²", "W/m²", "W/m²", "W/m²", "W/m²", "W/m²",
                             "W/m²", "W/m²", "W/m²", "°C", "°C", "°C", "°C", "°", "°", "°", "m/s", "m/s", "m/s", "°C",
                             "°C", "°C", "°C", "m³/m³", "m³/m³", "m³/m³", "m³/m³", "V", "mm"]
               },
               "24h": {"TITLES": ["Local", "Freq", "Data", "Hora", "Direção vento med ", "Direção vento max ",
                                  "Direção vento min ", "Velocidade vento med ", "Velocidade vento max ",
                                  "Velocidade vento min ", "ETP (H-S)"],
                       "UNITS": ["", "", "", "", "°", "°", "°", "m/s", "m/s", "m/s", "mm"]
                       }
           }
           }

if exists(CONFIGS_FILENAME):
    try:
        with open(CONFIGS_FILENAME) as configs_file:
            CONFIGS = json.load(configs_file)
            CONFIGS_LOADED = True
            print(f'{CONFIGS_FILENAME} loaded!')

    except:
        print(f'Error reading {CONFIGS_FILENAME} file.')
        try:
            if CREATE_CONFIGS_BKP:
                shutil.copy(CONFIGS_FILENAME, f'{CONFIGS_FILENAME}.{str(now()).split(".")[0]}.bkp')
                print(f'Backup for {CONFIGS_FILENAME} saved.')
                print(f'\nA new file {CONFIGS_FILENAME} will be created.')
        except:
            raise f'{CONFIGS_FILENAME} is corrupted and a backup cant proceed.' \
                  f'\nPlease do it manually and delete {CONFIGS_FILENAME}'

else:
    print(f'\nA new file {CONFIGS_FILENAME} will be created.')

for trials in range(LOGIN_LIMIT_TRY):
    address = CONFIGS['LOGIN']['ADDRESS']
    if not bool(address):
        address = input('ADDRESS (IP) > ')

    try:
        ftp = ftplib.FTP(address)
        CONFIGS['LOGIN']['ADDRESS'] = address
        break

    except:
        if CONFIGS_LOADED:
            print(f'Loaded ADDRESS [{address}] invalid! Please input to edit file.')
            CONFIGS['LOGIN']['ADDRESS'] = None
            UPDATE_CONFIGS = True
            continue
        print('ADDRESS invalid! Please input again.')

for trials in range(LOGIN_LIMIT_TRY):
    user, key = CONFIGS['LOGIN']['USER'], CONFIGS['LOGIN']['KEY']

    if not bool(user):
        user = input('USER > ')
    if not bool(key):
        key = input('KEY > ')

    try:
        print(ftp.login(user, key))
        print(ftp.getwelcome())

        CONFIGS['LOGIN']['USER'] = user
        while not CONFIGS['LOGIN']['KEY']:
            answer = input('Save KEY? [Y/N] > ').lower()
            if 'n' in answer:
                break
            if 'y' in answer:
                CONFIGS['LOGIN']['KEY'] = key
                UPDATE_CONFIGS = True
                break
        break

    except:
        if CONFIGS_LOADED:
            print(f'Loaded USER or KEY invalid! Please input to edit file.')
            CONFIGS['LOGIN']['USER'] = None
            CONFIGS['LOGIN']['KEY'] = None
            UPDATE_CONFIGS = True
            continue

        print('USER or KEY invalid! Please input again.')

for trials in range(LOGIN_LIMIT_TRY):
    ftp_path = CONFIGS['FTP_PATH']
    if not bool(ftp_path):
        ftp_path = input('FTP_PATH > ')

    try:
        print(f'{ftp.cwd(ftp_path)} -> {ftp_path}')
        CONFIGS['FTP_PATH'] = ftp_path
        break

    except:
        if CONFIGS_LOADED:
            print(f'Loaded PATH [{ftp_path}] invalid! Please input to edit file.')
            CONFIGS['FTP_PATH'] = None
            UPDATE_CONFIGS = True
            continue
        print('FTP_PATH invalid! Please input again.')

if not CONFIGS['CSV_OUTPUT_PATH']:
    CONFIGS['CSV_OUTPUT_PATH'] = DEFAULT_CSV_OUTPUT_PATH
    UPDATE_CONFIGS = True

if not isdir(CONFIGS['CSV_OUTPUT_PATH']):
    try:
        mkdir(CONFIGS['CSV_OUTPUT_PATH'])
        UPDATE_CONFIGS = True
    except:
        raise TypeError(f'CSV_OUTPUT_PATH: {CONFIGS["CSV_OUTPUT_PATH"]} is invalid!')

if not CONFIGS_LOADED or UPDATE_CONFIGS:
    try:
        with open(CONFIGS_FILENAME, 'w') as configs_file:
            json.dump(CONFIGS, configs_file, indent=2)
            print(f'{CONFIGS_FILENAME} updated!')

    except:
        raise f'{CONFIGS_FILENAME} cant be saved!'

try:
    print(f"Listing files...")
    filenames = sorted(ftp.nlst())
    print(f"[{len(filenames)}] files listed!")

    while True:
        interval = input('Input datetime interval [YYYY/MM/DD HH:mm - YYYY/MM/DD HH:mm] > ').lower()\
            .replace(' ', '').replace('/', '').replace(':', '').replace('[', '').replace(']', '').split('-')
        if any(interval):
            if type(interval) is list:
                if len(interval) == 2:
                    if len(interval[0]) == 12 and len(interval[1]) == 12:
                        if interval[0].isnumeric() and interval[1].isnumeric():
                            if int(interval[0]) <= int(interval[1]):
                                break

        print('Invalid interval! Please input again.')

    while True:
        rate = input(f'Select rate {list(CONFIGS["SAMPLE_FORM"].keys())} > ').lower().replace(' ', '').replace('\n', '')
        if rate in list(CONFIGS["SAMPLE_FORM"].keys()):
            break
        print('Invalid rate! Please input again.')

    print('Indexing samples...')
    samples = []
    for filename in filenames:
        if not rate == filename.replace('.txt', '').split('_')[-3]:
            continue

        file_time = ''.join(filename.replace('.txt', '').split('_')[-2:])
        if int(interval[0]) <= int(file_time) <= int(interval[1]):
            ftp.retrlines("RETR " + filename, lambda string_data: samples.append(string_data.split(',')))

    if not any(samples):
        print('No samples in interval.')
        quit()

    print(f'[{len(samples)}] samples ({rate} rate) in interval.'
          f'\n  Older sample -> {samples[0][2].replace("-", "/")} - {samples[0][3]} GMT+0'
          f'\n  Newer sample -> {samples[-1][2].replace("-", "/")} - {samples[-1][3]} GMT+0')

    csv_filename = f'{CONFIGS["FTP_PATH"].split("/")[-1]}-{rate}-{hex(int(str(now()).split(".")[0]))[2:]}.csv'

    print(f'Saving "{csv_filename}" in "{CONFIGS["CSV_OUTPUT_PATH"]}"')
    with open(f'{CONFIGS["CSV_OUTPUT_PATH"]}/{csv_filename}', 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(CONFIGS['SAMPLE_FORM'][rate]['TITLES'])
        writer.writerows(samples)

except ftplib.error_perm as resp:
    raise resp

except KeyboardInterrupt:
    raise KeyboardInterrupt
