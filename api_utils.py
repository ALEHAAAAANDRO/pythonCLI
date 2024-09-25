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

    packages2_dict = {pkg['name']: pkg for pkg in packages2}

    packages_only_in_branch1 = []

    for pkg1 in packages1:
        pkg2 = packages2_dict.get(pkg1['name'])
        if not pkg2:
            packages_only_in_branch1.append(pkg1)

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

        if compare_versions_with_mixed_segments(pkg1.get('epoch', '0'), pkg1['version'], pkg1['release'],
                                                pkg2.get('epoch', '0'), pkg2['version'], pkg2['release']):
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

def compare_versions_with_mixed_segments(epoch1, version1, release1, epoch2, version2, release2):
    if epoch1 != epoch2:
        return int(epoch1) > int(epoch2)

    version1_segments = split_version_to_segments(version1)
    version2_segments = split_version_to_segments(version2)

    version_comparison = compare_segments(version1_segments, version2_segments)
    if version_comparison != 0:
        return version_comparison > 0

    release1_segments = split_version_to_segments(release1)
    release2_segments = split_version_to_segments(release2)

    return compare_segments(release1_segments, release2_segments) > 0


def split_version_to_segments(version: str) -> list:
    return [int(s) if s.isdigit() else s for s in re.split(r'(\d+)', version) if s]

def compare_segments(segments1, segments2):
    for seg1, seg2 in zip(segments1, segments2):
        if type(seg1) == type(seg2):
            if seg1 > seg2:
                return 1
            elif seg1 < seg2:
                return -1
        else:
            if isinstance(seg1, int):
                return -1
            else:
                return 1

    if len(segments1) > len(segments2):
        return 1
    elif len(segments1) < len(segments2):
        return -1

    return 0