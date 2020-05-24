# Libraries
from api import simple_get
from bs4 import BeautifulSoup
import json

# Global Variables
URL_GPU = "https://www.notebookcheck.net/Mobile-Graphics-Cards-Benchmark-List.844.0.html?type=&sort=&showClassDescription=1&deskornote=2&perfrating=1&or=0&showBars=1&3dmark13_ice_gpu=1&3dmark13_cloud=1&3dmark13_cloud_gpu=1&3dmark13_fire=1&3dmark13_fire_gpu=1&3dmark13_time_spy=1&3dmark13_time_spy_gpu=1&3dmark11=1&3dmark11_gpu=1&vantage3dmark=1&vantage3dmarkgpu=1&3dmark06=1&3dmark01=1&glbenchmark=1&gfxbench30=1&gfxbench31=1&basemarkx11_med=1&basemarkx11_high=1&heaven3_dx=1&valley_dx=1&cb15_ogl=1&cinebench10_ogl=1&computemark_result=1&luxmark_sala=1&gpu_fullname=1&architecture=1&pixelshaders=1&vertexshaders=1&corespeed=1&shaderspeed=1&boostspeed=1&memoryspeed=1&memorybus=1&memorytype=1&directx=1&opengl=1&technology=1"


# Functions
def get_bench_score(html):
    try:
        return html.find('div').find('span', class_='bl_ch_value').find('span').get_text()
    except AttributeError as e:
        return None


def convert_emptystring(s):
    return None if s == "" else s


def scrape_gpu():
    raw_html = simple_get(URL_GPU)
    html = BeautifulSoup(raw_html, 'html.parser')
    table = html.find_all('table')[0]
    gpus_html = table.find_all("tr", {"class": ["desk_odd", "desk_even", "odd", "even", "smartphone_odd", "smartphone_even"]})
    gpus_list = []
    for gpu in gpus_html:
        try:
            model = gpu.find('td', class_='specs fullname').find('a').get_text()
        except AttributeError as e:
            model = gpu.find('td', class_='specs fullname').get_text()

        specs = [el.text for el in gpu.select("td[class=specs]")]

        # Benchmarks
        bench_3dmark = gpu.find_all('td', class_='value bv_201')
        bench_3dmark11 = gpu.find_all('td', class_='value bv_73')
        bench_3dmarkvantage = gpu.find_all('td', class_='value bv_37')

        gpus_list.append({
            "pos": gpu.find('td', class_='specs poslabel').find('label').find('span').get_text(),
            "model": model,
            "architecture": convert_emptystring(gpu.find('td', class_='specs sorttable_codename').get_text()),
            "pixel_shaders": convert_emptystring(specs[0]),
            "core_speed": convert_emptystring(specs[1]),
            "shader_speed": convert_emptystring(specs[2]),
            "boost": convert_emptystring(specs[3]),
            "memory_speed": convert_emptystring(specs[4]),
            "memory_bus": convert_emptystring(specs[5]),
            "memory_type": convert_emptystring(specs[6]),
            "directx": convert_emptystring(specs[7]),
            "opengl": convert_emptystring(specs[8]),
            "process_nm": convert_emptystring(specs[9]),
            "bench_3dmark_icestorm": get_bench_score(bench_3dmark[0]),
            "bench_3dmark_cloudgate": get_bench_score(bench_3dmark[1]),
            "bench_3dmark_cloudgate_gpu": get_bench_score(bench_3dmark[2]),
            "bench_3dmark_cloudgate_firestrike": get_bench_score(bench_3dmark[3]),
            "bench_3dmark_cloudgate_firestrike_graphics": get_bench_score(bench_3dmark[4]),
            "bench_3dmark_cloudgate_timespy": get_bench_score(bench_3dmark[5]),
            "bench_3dmark_cloudgate_timespy_graphics": get_bench_score(bench_3dmark[6]),
            "bench_3dmark11": get_bench_score(bench_3dmark11[0]),
            "bench_3dmark11_gpu": get_bench_score(bench_3dmark11[1]),
            "bench_3dmarkvantage": get_bench_score(bench_3dmarkvantage[0]),
            "bench_3dmarkvantage_gpu": get_bench_score(bench_3dmarkvantage[1]),
            "bench_3dmark06": get_bench_score(gpu.find('td', class_='value bv_4')),
            "bench_3dmark01": get_bench_score(gpu.find('td', class_='value bv_1')),
            "bench_gfxbench": get_bench_score(gpu.find('td', class_='value bv_216')),
            "bench_gfxbench30": get_bench_score(gpu.find('td', class_='value bv_260')),
            "bench_gfxbench31": get_bench_score(gpu.find('td', class_='value bv_327')),
            "bench_unigineheaven": get_bench_score(gpu.find('td', class_='value bv_178')),
            "bench_uniginevalley": get_bench_score(gpu.find('td', class_='value bv_358')),
            "bench_cinebench15": get_bench_score(gpu.find('td', class_='value bv_244')),
            "bench_cinebench10": get_bench_score(gpu.find('td', class_='value bv_22')),
            "bench_computemark": get_bench_score(gpu.find('td', class_='value bv_147')),
            "bench_luxmark": get_bench_score(gpu.find('td', class_='value bv_146'))
        })

    return gpus_list


if __name__ == "__main__":
    gpus = scrape_gpu()
    print("Fetched " + str(len(gpus)) + " GPUs' informations")

    with open('gpus.json', 'w') as outfile:
        json.dump(gpus, outfile)
