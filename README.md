# AUtomated DOcking 4 RIsk ASsessment

## Installation

### Clone repository

To install **AUDO4RIAS**, type this command into your terminal:

`git clone https://github.com/mungowz/AUDO4RIAS.git`

The GitHub repository of the project will be cloned into a local directory chosen by user.

### External dependencies

In the following, external dependencies are listed. 
We strongly recommend you to follow the installation instructions of the softwares below mentioned.

- [_MGLTools v1.5.6_](https://ccsb.scripps.edu/mgltools/downloads/)
- [_ADFR suite v1.0_]( https://ccsb.scripps.edu/adfr/downloads/)
- [_AutoDock Vina_](https://vina.scripps.edu/downloads/) (version 1.1.2)
- [_GNINA_](https://github.com/gnina/gnina)
- [_Open Babel_](https://snapcraft.io/install/openbabel/ubuntu)
- _XTerm_: `sudo apt-get install xterm`

Using Python3.8+ version,
- _Tkinter_: `sudo apt-get install python3-tk`
- _pip_: `sudo apt-get install python3-pip`



**N.B.:** For Linux users, **bin directories of MGLTools, ADFRsuite and AutoDock Vina**, which are placed in the corresponding installation directories, **must** be added to your global enviroment variable **`$PATH`**.

So, modify `\home\<username>\.bashrc` file adding at the corresponding paths for these directories.

Once updated `.bashrc` file, type this command for applying the changes:

`source \home\<username>\.bashrc`

### Internal dependencies
Internal dependencies, which correspond to python packages and libraries, can be installed by typing this command into your terminal:

`pip install -r requirements.txt`
