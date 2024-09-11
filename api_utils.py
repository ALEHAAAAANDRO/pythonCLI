# api_utils.py
import requests

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