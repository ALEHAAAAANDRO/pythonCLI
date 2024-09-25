#!/usr/bin/env python3

import argparse
from api_utils import get_architectures, compare_packages, compare_versions_and_releases

branch1 = None
branch2 = None
selected_arch = None

def main() -> None:
    global branch1, branch2

    parser = argparse.ArgumentParser(
        description="Retrieves lists of binary packages for two branches of ALT Linux."
    )
    parser.add_argument(
        "branch1", type=str, help="The name of the first branch (for example, sisyphus)"
    )
    parser.add_argument(
        "branch2", type=str, help="The name of the second branch (for example, p10)"
    )
    args = parser.parse_args()

    branch1 = args.branch1
    branch2 = args.branch2

def menu():
    global selected_arch

    while True:
        print("\nMenu:")
        print("1. Choose an architecture")
        print("2. Packages missing in the 2nd branch")
        print("3. Packages missing in 1 branch")
        print("4. Packages whose version-release is higher in 1 branch")
        print("5. Packages whose version-release is higher in the 2nd branch")
        print("6. Exit")

        choice = input("Select an option (1-6): ")

        if choice == '1':
            architectures1 = get_architectures(branch1)
            architectures2 = get_architectures(branch2)

            all_architectures = list(architectures1.union(architectures2))

            if not all_architectures:
                print("The architectures for the specified branches could not be found.")
                continue

            print("\nAvailable architectures from branches:")
            for i, arch in enumerate(all_architectures, start=1):
                print(f"{i}. {arch}")

            try:
                arch_choice = int(input("Choose an architecture (number): ")) - 1
                if 0 <= arch_choice < len(all_architectures):
                    selected_arch = all_architectures[arch_choice]
                    print(f"You have chosen the architecture: {selected_arch}")
                else:
                    print("Incorrect choice. Try again.")
                    continue
            except ValueError:
                print("Please enter the correct number.")
                continue

        elif choice == '2':
            if not selected_arch:
                print("First, select the architecture in step 1.")
                continue

            missing_packages = compare_packages(branch1, branch2, selected_arch, 1)
            print("\nPackages that are in the first branch, but are missing in the second:")
            for pkg in missing_packages:
                print(f"- {pkg['name']} {pkg['version']}-{pkg['release']} {pkg['arch']}")

        elif choice == '3':
            if not selected_arch:
                print("First, select the architecture in step 1.")
                continue

            missing_packages_reverse = compare_packages(branch2, branch1, selected_arch, 0)
            print("\nPackages that are in the second branch, but are missing in the first:")
            for pkg in missing_packages_reverse:
                print(f"- {pkg['name']} {pkg['version']}-{pkg['release']} {pkg['arch']}")

        elif choice == '4':
            if not selected_arch:
                print("The architecture is not selected. First, select the architecture in step 1.")
                continue
            compare_versions_and_releases(branch1, branch2, selected_arch, 1)


        elif choice == '5':
            if not selected_arch:
                print("The architecture is not selected. First, select the architecture in step 1.")
                continue
            compare_versions_and_releases(branch2, branch1, selected_arch, 0)


        elif choice == '6':
            print("Exiting the program.")
            break

        else:
            print("Incorrect choice. Try again.")


if __name__ == "__main__":
    main()
    menu()