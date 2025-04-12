import yaml


def generate_case(yml_file_path):
    with open(yml_file_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    return data

if __name__ == '__main__':
    data = generate_case('api_data.yml')
    audio = data['audio']
    for v in audio :
        print(v)