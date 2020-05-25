# Libraries
from api import simple_get
from bs4 import BeautifulSoup
from constants import URL_GPU
from utils import get_bench_score, convert_emptystring
import json


# Function(s)
def scrape_gpu():
    print("Requesting...")
    raw_html = simple_get(URL_GPU)

    if raw_html is None:
        print("NotebookCheck sometimes return an invalid HTML. Please try again!")
        return
    else:
        print("Request success!")

    print("Scraping...")
    html = BeautifulSoup(raw_html, 'html.parser')
    table = html.find_all('table')[0]
    gpus_html = table.find_all(
        "tr",
        {"class": ["desk_odd", "desk_even", "odd", "even", "smartphone_odd", "smartphone_even"]}
    )
    gpus_list = []
    for gpu in gpus_html:
        try:
            model = gpu.find('td', class_='specs fullname').find('a').get_text()
        except AttributeError as e:
            model = gpu.find('td', class_='specs fullname').get_text()

        specs_sorttable = [el.text for el in gpu.find_all('td', class_='specs sorttable_codename')]
        specs = [el.text for el in gpu.select("td[class=specs]")]

        # Benchmarks with multiple categories
        bench_3dmark = gpu.find_all('td', class_='value bv_201')
        bench_3dmark11 = gpu.find_all('td', class_='value bv_73')
        bench_3dmarkvantage = gpu.find_all('td', class_='value bv_37')
        bench_basemark = gpu.find_all('td', class_='value bv_267')

        gpus_list.append({
            "Pos": gpu.find('td', class_='specs poslabel').find('label').find('span').get_text(),
            "Model": model,
            "Codename": convert_emptystring(specs_sorttable[0]),
            "Architecture": convert_emptystring(specs_sorttable[1]),
            "Pixel Shaders": convert_emptystring(specs[0]),
            "Core Speed": convert_emptystring(specs[1]),
            "Shader Speed": convert_emptystring(specs[2]),
            "Boost / Turbo": convert_emptystring(specs[3]),
            "Memory Speed": convert_emptystring(specs[4]),
            "Memory Bus": convert_emptystring(specs[5]),
            "Memory Type": convert_emptystring(specs[6]),
            "DirectX": convert_emptystring(specs[7]),
            "OpenGL": convert_emptystring(specs[8]),
            "Process (nm)": convert_emptystring(specs[9]),
            "Days old": convert_emptystring(specs[10]),
            "3DMark Ice Storm GPU": get_bench_score(bench_3dmark[0]),
            "3DMark Cloud Gate Standard Score": get_bench_score(bench_3dmark[1]),
            "3DMark Cloud Gate GPU": get_bench_score(bench_3dmark[2]),
            "3DMark Fire Strike Score": get_bench_score(bench_3dmark[3]),
            "3DMark Fire Strike Graphics": get_bench_score(bench_3dmark[4]),
            "3DMark Time Spy Score": get_bench_score(bench_3dmark[5]),
            "3DMark Time Spy Graphics": get_bench_score(bench_3dmark[6]),
            "3DMark11 P": get_bench_score(bench_3dmark11[0]),
            "3DMark11 P GPU": get_bench_score(bench_3dmark11[1]),
            "3DMark Vantage P": get_bench_score(bench_3dmarkvantage[0]),
            "3DMark Vant. P GPU": get_bench_score(bench_3dmarkvantage[1]),
            "3DMark06": get_bench_score(gpu.find('td', class_='value bv_4')),
            "3DMark01": get_bench_score(gpu.find('td', class_='value bv_1')),
            "GFXBench": get_bench_score(gpu.find('td', class_='value bv_216')),
            "GFXBench 3.0 Manhattan Offscreen OGL": get_bench_score(gpu.find('td', class_='value bv_260')),
            "GFXBench 3.1 Manhattan ES 3.1 Offscreen": get_bench_score(gpu.find('td', class_='value bv_327')),
            "Basemark X 1.1 Medium Quality": get_bench_score(bench_basemark[0]),
            "Basemark X 1.1 High Quality": get_bench_score(bench_basemark[1]),
            "Unigine Heaven 3.0 DX 11, Normal Tessellation, High Shaders": get_bench_score(gpu.find('td', class_='value bv_178')),
            "Unigine Valley 1.0 Extreme HD DirectX": get_bench_score(gpu.find('td', class_='value bv_358')),
            "Cinebench R15 OpenGL 64Bit": get_bench_score(gpu.find('td', class_='value bv_244')),
            "Cinebench R10 32Bit OpenGL": get_bench_score(gpu.find('td', class_='value bv_22')),
            "ComputeMark v2.1 Normal, Score": get_bench_score(gpu.find('td', class_='value bv_147')),
            "LuxMark v2.0 64Bit Sala GPUs-only": get_bench_score(gpu.find('td', class_='value bv_146'))
        })

    return gpus_list


if __name__ == "__main__":
    gpus = scrape_gpu()
    print("Scrapped " + str(len(gpus)) + " GPUs' data")

    print("Dumping result to json file...")
    with open('gpus.json', 'w') as outfile:
        json.dump(gpus, outfile)
    print("Done")
