# Libraries
from api import simple_get
from bs4 import BeautifulSoup
from constants import URL_CPU
from utils import get_bench_score, convert_emptystring
import json


# Function(s)
def scrape_cpu():
    print("Requesting...")
    raw_html = simple_get(URL_CPU)

    if raw_html is None:
        print("NotebookCheck sometimes return an invalid HTML. Please try again!")
        return
    else:
        print("Request success!")

    print("Scraping...")
    html = BeautifulSoup(raw_html, 'html.parser')
    table = html.find_all('table')[0]
    cpus_html = table.find_all(
        "tr",
        {"class": ["desk_odd", "desk_even", "odd", "even", "smartphone_odd", "smartphone_even"]}
    )
    cpus_list = []
    for cpu in cpus_html:
        specs = cpu.select("td[class=specs]")

        try:
            model = specs[0].find('a').get_text()
        except AttributeError as e:
            model = specs[0].get_text()

        if specs[9].find('img'):
            is_bit64 = True
        else:
            is_bit64 = False

        try:
            graphics_card = specs[10].find('a').get_text() if not is_bit64 else specs[11].find('a').get_text()
        except AttributeError as e:
            graphics_card = specs[10].get_text() if not is_bit64 else specs[11].get_text()


        # Benchmarks with multiple categories
        bench_cinebench10 = cpu.find_all('td', class_="value bv_22")
        bench_cinebench11 = cpu.find_all('td', class_="value bv_62")
        bench_cinebench15 = cpu.find_all('td', class_="value bv_244")
        bench_cinebench20 = cpu.find_all('td', class_="value bv_671")
        bench_wprime = cpu.find_all('td', class_="value bv_50")
        bench_x264 = cpu.find_all('td', class_="value bv_92")
        bench_truecrypt = cpu.find_all('td', class_="value bv_93")
        bench_7zip = cpu.find_all('td', class_="value bv_552")
        bench_geekbench3 = cpu.find_all('td', class_="value bv_235")
        bench_geekbench4 = cpu.find_all('td', class_="value bv_440")
        bench_geekbench5 = cpu.find_all('td', class_="value bv_693")
        bench_geekbench51 = cpu.find_all('td', class_="value bv_717")


        cpus_list.append({
            "Pos": cpu.find('td', class_='specs poslabel').find('label').find('span').get_text(),
            "Model": model,
            "Codename": cpu.find('td', class_='sorttable_codename').get_text(),
            "Series": convert_emptystring(specs[1].get_text()),
            "L2 Cache + L3 Cache": convert_emptystring(specs[2].get_text()),
            "FSB / QPI": convert_emptystring(specs[3].get_text()),
            "TDP": convert_emptystring(specs[4].get_text()),
            "MHz - Turbo": convert_emptystring(specs[5].get_text()),
            "Cores / Threads": convert_emptystring(specs[6].get_text()),
            "Process (nm)": convert_emptystring(specs[7].get_text()),
            "Architecture": convert_emptystring(specs[8].get_text()),
            "64 Bit": is_bit64,
            "Days old": specs[9].get_text() if not is_bit64 else specs[10].get_text(),
            "Graphics Card": graphics_card,
            "3DMark06 CPU": get_bench_score(cpu.find('td', class_='value bv_5')),
            'Cinebench R10 32Bit Single': get_bench_score(bench_cinebench10[0]),
            "Cinebench R10 32Bit Multi": get_bench_score(bench_cinebench10[1]),
            "Cinebench R11.5 CPU Single 64Bit": get_bench_score(bench_cinebench11[0]),
            "Cinebench R11.5 CPU 64Bit": get_bench_score(bench_cinebench11[1]),
            "Cinebench R15 CPU Single 64Bit": get_bench_score(bench_cinebench15[0]),
            "Cinebench R15 CPU Multi 64Bit": get_bench_score(bench_cinebench15[1]),
            "Cinebench R20 Single": get_bench_score(bench_cinebench20[0]),
            "Cinebench R20": get_bench_score(bench_cinebench20[1]),
            "SuperPI 1M": get_bench_score(cpu.find('td', class_='value bv_6')),
            "SuperPI 32M": get_bench_score(cpu.find('td', class_='value bv_8')),
            "wPrime 32": get_bench_score(bench_wprime[0]),
            "wPrime 1024": get_bench_score(bench_wprime[1]),
            "WinRAR 4.0": get_bench_score(cpu.find('td', class_='value bv_91')),
            "x264 Pass 1": get_bench_score(bench_x264[0]),
            "x264 Pass 2": get_bench_score(bench_x264[1]),
            "x265": get_bench_score(cpu.find('td', class_='value bv_560')),
            "TrueCrypt AES": get_bench_score(bench_truecrypt[0]),
            "TrueCrypt Twofish": get_bench_score(bench_truecrypt[1]),
            "TrueCrypt Serpent": get_bench_score(bench_truecrypt[2]),
            "Blender": get_bench_score(cpu.find('td', class_='value bv_496')),
            "7-Zip Single": get_bench_score(bench_7zip[0]),
            "7-Zip" : get_bench_score(bench_7zip[1]),
            "Geekbench 2": get_bench_score(cpu.find('td', class_='value bv_136')),
            "Geekbench 3 32 Bit Single-Core Score": get_bench_score(bench_geekbench3[0]),
            "Geekbench 3 32 Bit Multi-Core Score": get_bench_score(bench_geekbench3[1]),
            "Geekbench 4.4 64 Bit Single-Core Score": get_bench_score(bench_geekbench4[0]),
            "Geekbench 4.4 64 Bit Multi-Core Score": get_bench_score(bench_geekbench4[1]),
            "Geekbench 5 64 Bit Single-Core Score": get_bench_score(bench_geekbench5[0]),
            "Geekbench 5 64 Bit Multi-Core Score": get_bench_score(bench_geekbench5[1]),
            "Geekbench 5.1 64 Bit Single-Core Score": get_bench_score(bench_geekbench51[0]),
            "Geekbench 5.1 64 Bit Multi-Core Score": get_bench_score(bench_geekbench51[1]),
            "PassMark PerformanceTest Mobile V1 CPU Tests": get_bench_score(cpu.find('td', class_='value bv_200')),
            "Sunspider 1.0 Total Score": get_bench_score(cpu.find('td', class_='value bv_124')),
            "Octane V2 Total Score": get_bench_score(cpu.find('td', class_='value bv_253')),
            "Jetstream 2": get_bench_score(cpu.find('td', class_='value bv_680')),
            "Speedometer": get_bench_score(cpu.find('td', class_='value bv_666')),
            "WebXPRT 3": get_bench_score(cpu.find('td', class_='value bv_550')),
        })

    return cpus_list


if __name__ == "__main__":
    cpus = scrape_cpu()
    print("Scrapped " + str(len(cpus)) + " CPUs' data")

    print("Dumping result to json file...")
    with open('cpus.json', 'w') as outfile:
        json.dump(cpus, outfile)
    print("Done")
