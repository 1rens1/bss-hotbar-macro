# BSS Hotbar Macro
<p align="center">
    <img src="https://cdn.horizon.pics/nY0fuTnDWS" alt="Macro screenshot preview" />
</p>

A simple hotbar macro built with Python tkinter and pynput!

## Installation from executable
* Go to the [releases tab](https://github.com/1rens1/bss-hotbar-macro/releases) and download the latest `BSS-Hotbar-Macro.exe`.
* Run the macro and ignore anti-virus warnings.

Note: See [Virus Warnings](#virus-warnings)

## Installation from source
* Clone the repository

    ```shell
    $ git clone https://github.com/1rens1/bss-hotbar-macro.git
    $ cd bss-hotbar-macro
    ```
* Install the required dependencies
  ```shell
  $ pip install -r requirements.txt
  ```
* Run the script
  ```shell
  $ python main.py
  # or
  $ python3 main.py
  ```

## VIRUS WARNINGS

### Executable

The executable is generated using [`pyinstaller`](https://pyinstaller.org/), a popular tool for converting Python scripts into standalone executables. Some anti-virus software may flag the executable as a trojan, but this is also a false positive and you can safely run the macro.

See this [GitHub issue comment](https://github.com/pyinstaller/pyinstaller/issues/5854#issuecomment-846312429) for more information.

### Python Source
Anti-virus programs warns you that the python script is a key logger, this is related to the `pynput` Python module. This warning is a false positive, and the script is not a virus.

The script only needs the `pynput` module to simulate key presses and listen to the start/stop hotkey

If you have any concerns feel free to explore the [source code](main.py).

### Exclude macro from anti-virus
To resolve false alarms from your anti-virus program, you can add an exclusion for the cloned repository folder. For example, you can follow these steps to [add an exclusion in Windows Security](https://support.microsoft.com/en-us/windows/add-an-exclusion-to-windows-security-811816c0-4dfd-af4a-47e4-c301afe13b26).

Note: The exclusion methods may vary depending on your anti-virus program.
