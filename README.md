# pythonCLI

This project is a command-line tool that allows you to work with binary package lists from different branches of ALT Linux. The tool can compare packages, filter them by architecture, and provide insights on version differences between two branches.

## Features

- Fetch binary packages from ALT Linux branches.
- Filter packages by architecture.
- Compare package lists between two branches.
- Identify packages missing in one branch but present in another.
- Compare version-release numbers between packages in different branches.

## Prerequisites

- Python 3.8 or later

## Installation

### Step 1: Clone the Repository

Clone the project repository:

```bash
git clone https://github.com/ALEHAAAAANDRO/pythonCLI.git
cd pythonCLI
```

### Step 2: Install


```bash
sudo ./install.sh
```

## Usage

### Basic Command

Run the command-line tool using the following syntax:

```bash
pythonCLI <branch1> <branch2>
```

Replace `<branch1>` and `<branch2>` with the names of the ALT Linux branches you wish to compare (e.g., `sisyphus` and `p10`).

### Example

```bash
pythonCLI sisyphus p10
```

### Main Menu

After launching, you will see the main menu with the following options:

1. Select Architecture
2. Packages missing from the second branch
3. Packages missing from the first branch
4. Packages with higher version-release in the first branch
5. Packages with higher version-release in the second branch
6. Exit

Choose the desired option by entering the corresponding number.

### Advanced Usage

1. **Select Architecture:** Choose the architecture you want to filter packages by.
2. **Compare Packages:** Identify packages present in one branch but missing in the other.
3. **Compare Versions:** Compare the version-release of packages between two branches to identify those with higher versions.

## Uninstallation

To uninstall the tool, remove the installed files:

```bash
sudo rm /usr/lib/python3/site-packages/api_utils.py
sudo rm /usr/local/bin/pythonCLI
```
