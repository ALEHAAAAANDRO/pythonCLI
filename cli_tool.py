# cli_tool.py
import argparse
from api_utils import get_packages, print_packages, get_architectures, compare_packages, compare_versions_and_releases

branch1 = None
branch2 = None
selected_arch = None

def main() -> None:
    global branch1, branch2

    parser = argparse.ArgumentParser(
        description="Получает списки бинарных пакетов для двух веток ALT Linux."
    )
    parser.add_argument(
        "branch1", type=str, help="Название первой ветки (например, sisyphus)"
    )
    parser.add_argument(
        "branch2", type=str, help="Название второй ветки (например, p10)"
    )
    args = parser.parse_args()

    branch1 = args.branch1
    branch2 = args.branch2

    #packages1 = get_packages(branch1)
    #packages2 = get_packages(branch2)

    # print_packages(branch1, packages1)
    # print()
    # print_packages(branch2, packages2)
    #
    # print(f"Все возможные архитектуры для ветки {branch1}:")
    # architectures1 = get_architectures(branch1)
    # print(', '.join(architectures1))
    #
    # print(f"\nВсе возможные архитектуры для ветки {branch2}:")
    # architectures2 = get_architectures(branch2)
    # print(', '.join(architectures2))


def menu():
    global selected_arch

    while True:
        print("\nМеню:")
        print("1. Выбрать архитектуру")
        print("2. Пакеты, отсутствующие во 2 ветке")
        print("3. Пакеты, отсутствующие в 1 ветке")
        print("4. Пакеты, version-release которых выше в 1 ветке")
        print("5. Пакеты, version-release которых выше во 2 ветке")
        print("6. Выход")

        choice = input("Выберите опцию (1-6): ")

        if choice == '1':
            architectures1 = get_architectures(branch1)
            architectures2 = get_architectures(branch2)

            all_architectures = list(architectures1.union(architectures2))

            if not all_architectures:
                print("Не удалось найти архитектуры для указанных веток.")
                continue

            print("\nДоступные архитектуры из веток:")
            for i, arch in enumerate(all_architectures, start=1):
                print(f"{i}. {arch}")

            try:
                arch_choice = int(input("Выберите архитектуру (номер): ")) - 1
                if 0 <= arch_choice < len(all_architectures):
                    selected_arch = all_architectures[arch_choice]
                    print(f"Вы выбрали архитектуру: {selected_arch}")
                else:
                    print("Некорректный выбор. Попробуйте снова.")
                    continue
            except ValueError:
                print("Пожалуйста, введите корректный номер.")
                continue

        elif choice == '2':
            if not selected_arch:
                print("Сначала выберите архитектуру в пункте 1.")
                continue

            missing_packages = compare_packages(branch1, branch2, selected_arch, 1)
            print("\nПакеты, которые есть в первой ветке, но отсутствуют во второй:")
            for pkg in missing_packages:
                print(f"- {pkg['name']} {pkg['version']}-{pkg['release']} {pkg['arch']}")

        elif choice == '3':
            if not selected_arch:
                print("Сначала выберите архитектуру в пункте 1.")
                continue

            missing_packages_reverse = compare_packages(branch2, branch1, selected_arch, 0)
            print("\nПакеты, которые есть во второй ветке, но отсутствуют в первой:")
            for pkg in missing_packages_reverse:
                print(f"- {pkg['name']} {pkg['version']}-{pkg['release']} {pkg['arch']}")

        elif choice == '4':
            if not selected_arch:
                print("Архитектура не выбрана. Сначала выберите архитектуру в пункте 1.")
                continue
            compare_versions_and_releases(branch1, branch2, selected_arch, 1)


        elif choice == '5':
            if not selected_arch:
                print("Архитектура не выбрана. Сначала выберите архитектуру в пункте 1.")
                continue
            compare_versions_and_releases(branch2, branch1, selected_arch, 0)


        elif choice == '6':
            print("Выход из программы.")
            break

        else:
            print("Некорректный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()
    menu()