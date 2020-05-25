def get_bench_score(html):
    try:
        return html.find('div').find('span', class_='bl_ch_value').find('span').get_text()
    except AttributeError as e:
        return None


def convert_emptystring(s):
    return None if s == "" else s
