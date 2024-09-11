# cli_tool.py
import argparse
from api_utils import get_packages, print_packages, get_architectures


def main() -> None:
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

    packages1 = get_packages(args.branch1)
    packages2 = get_packages(args.branch2)

    print_packages(args.branch1, packages1)
    print()
    print_packages(args.branch2, packages2)

    print(f"Все возможные архитектуры для ветки {args.branch1}:")
    architectures1 = get_architectures(args.branch1)
    print(', '.join(architectures1))

    print(f"\nВсе возможные архитектуры для ветки {args.branch2}:")
    architectures2 = get_architectures(args.branch2)
    print(', '.join(architectures2))

if __name__ == "__main__":
    main()
