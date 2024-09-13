import requests
import json
import os
import re

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
        print(f"Error when requesting data for a branch {branch}: {e}")
        return []

def print_packages(branch: str, packages: list) -> None:
    print(f"Packages for the branch {branch}:")
    filtered_packages = [pkg for pkg in packages if pkg['arch'] != 'aarch64']
    for package in filtered_packages[:10]:
        print(f"- {package['name']} {package['version']}-{package['release']} {package['arch']}")

def get_architectures(branch: str) -> set:
    packages = get_packages(branch)
    architectures = {pkg['arch'] for pkg in packages if isinstance(pkg, dict) and 'arch' in pkg}
    return architectures

def get_packages_arch(branch: str, arch: str) -> list:
    packages = get_packages(branch)
    return [pkg for pkg in packages if pkg.get('arch') == arch]

def compare_packages(branch1: str, branch2: str, arch: str, flag: int) -> list:
    packages1 = get_packages_arch(branch1, arch)
    packages2 = get_packages_arch(branch2, arch)

    packages_only_in_branch1 = [pkg for pkg in packages1 if pkg['name'] not in {p['name'] for p in packages2}]

    if flag == 1:
        filename = os.path.expanduser("~/missing_packages_from_second_branch.json")
    else:
        filename = os.path.expanduser("~/missing_packages_from_first_branch.json")

    try:
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(packages_only_in_branch1, file, ensure_ascii=False, indent=4)
        print(f"The results are saved to a file: {filename}")
    except IOError as e:
        print(f"Error saving the file: {e}")

    return packages_only_in_branch1

def compare_versions_and_releases(branch1: str, branch2: str, arch: str, flag: int) -> list:
    packages1 = get_packages_arch(branch1, arch)
    packages2 = get_packages_arch(branch2, arch)

    packages2_dict = {pkg['name']: pkg for pkg in packages2}

    higher_version_packages = []

    for pkg1 in packages1:
        pkg2 = packages2_dict.get(pkg1['name'])
        if not pkg2:
            continue

        version1_numbers = extract_numbers(pkg1['version'])
        version2_numbers = extract_numbers(pkg2['version'])

        if version1_numbers > version2_numbers:
            higher_version_packages.append(pkg1)
        elif version1_numbers == version2_numbers:
            release1_numbers = extract_numbers(pkg1['release'])
            release2_numbers = extract_numbers(pkg2['release'])

            if release1_numbers > release2_numbers:
                higher_version_packages.append(pkg1)

    if flag == 1:
        filename = os.path.expanduser("~/higher_version_packages_in_first_br.json")
    else:
        filename = os.path.expanduser("~/higher_version_packages_in_second_br.json")

    try:
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(higher_version_packages, file, ensure_ascii=False, indent=4)
        print(f"The results are saved to a file: {filename}")
    except IOError as e:
        print(f"Error saving the file: {e}")

    return higher_version_packages

def extract_numbers(text: str) -> tuple:
    numbers = re.findall(r'\d+', text)
    return tuple(map(int, numbers))