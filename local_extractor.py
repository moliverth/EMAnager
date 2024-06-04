
from pathlib import Path
from time import time as now
import tkinter
from tkinter.filedialog import askopenfilenames, asksaveasfilename
from tkinter.simpledialog import askstring
from tkinter.messagebox import showinfo, showerror, showwarning
from csv import writer as csvwritter

SAMPLE_HEADERS_BY_RATE = {
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

try:
    print(f"Selecting files...")
    filenames = askopenfilenames(title="Selecione os arquivos:",
                                 filetypes=[('text file', '*.txt')])
    if filenames is None or not any(filenames):
        print('Quitting...')
        quit()
    
    print(f"[{len(filenames)}] files selected!")

    try:
        preset_rate = filenames[0].split('_')[-3]
    except:
        preset_rate = ''

    while True:
        selected_rate = askstring('Input', 
                        f'Selecione a taxa {list(SAMPLE_HEADERS_BY_RATE.keys())}',
                        initialvalue=preset_rate)
        if selected_rate is None:
            print('Quitting...')
            quit()
        if selected_rate in list(SAMPLE_HEADERS_BY_RATE.keys()):
            break

        print('Invalid rate! Please input again.')
        showerror(title='Error', message='Entrada inválida!')

    print('Indexing samples...')
    samples = []
    for filename in filenames:
        try:
            filename_rate = filename.split('_')[-3]
        except:
            filename_rate = ''

        if not selected_rate == filename_rate:
            print(f'[WARN] [{Path(filename).stem}] incompatible rate' )
            showwarning(title='Warning', message=f'[{Path(filename).stem}] possui taxa incompatível.')
            continue

        sample = Path(filename).read_text().split(',')

        if not len(sample) == len(SAMPLE_HEADERS_BY_RATE[selected_rate]['TITLES']):
            print(f'[WARN] [{Path(filename).stem}] imcompatible number of rows' )
            showwarning(title='Warning', message=f'[{Path(filename).stem}] possui número incompatível de colunas.')
            continue

        samples.append(sample)

    if not any(samples):
        print('No samples retrieved, quitting!')
        showerror(title='Error', message='Nenhuma amostra recuperada.')
        quit()

    print(f'[{len(samples)}] samples ({selected_rate} rate) in interval.'
          f'\n  Older sample -> {samples[0][2].replace("-", "/")} - {samples[0][3]} GMT+0'
          f'\n  Newer sample -> {samples[-1][2].replace("-", "/")} - {samples[-1][3]} GMT+0')

    output_default_filename = f'{samples[0][2]}-{samples[-1][2]}-{selected_rate}-{hex(int(str(now()).split(".")[0]))[2:]}.csv'
    output_path = Path(asksaveasfilename(filetypes=[("csv file", ".csv")],
                                         defaultextension=".csv",
                                         initialfile=output_default_filename)).resolve()
    
    print(f'Writting [{output_path}]')
    with output_path.open("w") as csv_file:
        writer = csvwritter(csv_file)
        writer.writerow(SAMPLE_HEADERS_BY_RATE[selected_rate]['TITLES'])
        writer.writerows(samples)

    print('Saved!')

except KeyboardInterrupt:
    raise KeyboardInterrupt