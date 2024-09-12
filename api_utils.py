# api_utils.py
import requests
import json
import os

# get packages from branch
def get_packages(branch: str) -> list:
    url = f"https://rdb.altlinux.org/api/export/branch_binary_packages/{branch}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if isinstance(data, dict) and 'packages' in data:
            return data['packages']
        else:
            return data
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе данных для ветки {branch}: {e}")
        return []

# print 50 packages
def print_packages(branch: str, packages: list) -> None:
    print(f"Пакеты для ветки {branch}:")
    filtered_packages = [pkg for pkg in packages if pkg['arch'] != 'aarch64']
    for package in filtered_packages[:10]:
        print(f"- {package['name']} {package['version']}-{package['release']} {package['arch']}")

# get all arch from branch
def get_architectures(branch: str) -> set:
    packages = get_packages(branch)
    architectures = {pkg['arch'] for pkg in packages if isinstance(pkg, dict) and 'arch' in pkg}
    return architectures

def get_packages_arch(branch: str, arch: str) -> list:
    packages = get_packages(branch)
    return [pkg for pkg in packages if pkg.get('arch') == arch]

def compare_packages(branch1: str, branch2: str, arch: str) -> list:
    packages1 = get_packages_arch(branch1, arch)
    packages2 = get_packages_arch(branch2, arch)

    packages_only_in_branch1 = [pkg for pkg in packages1 if pkg['name'] not in {p['name'] for p in packages2}]

    filename = os.path.expanduser("~/missing_packages_from_second_branch.json")

    try:
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(packages_only_in_branch1, file, ensure_ascii=False, indent=4)
        print(f"Результаты сохранены в файл: {filename}")
    except IOError as e:
        print(f"Ошибка при сохранении файла: {e}")

    return packages_only_in_branch1