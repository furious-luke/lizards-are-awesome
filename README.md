# lizards-are-awesome

A Docker based workflow for performing a Plink/fastStructure analysis from Excel data.


## Overview

This software seeks to ease much the manual labour involved in preparing data for
running with Plink and fastStructure. Most of the work, besides the mentioned
external packages, is done with a Python script. The primary operations
performed by the script are:

 1. Duplicating the input data.
 2. Performing a substitution on certain values in the duplicated data.
 3. Indpenendantly indexing both sets of data.
 4. Combining the original and duplicated data.
 5. Sorting on the combined index.
 6. Transposing the combined data.
 7. Outputting to a Plink compatible format.

Whereas before these steps would be carred out manually using various software
packages, they are now performed automatically.

In addition to the main conversion operation, there are additional functions
to perform analysis runs of Plink and fastStructre, passing the data files
between the two programs automatically.


## Design Decisions

### Why Docker?

`Plink` is written for Linux based operating systems. As such on a Linux system
all operations could be performed directly, without the need for any kind of
virtualisation layer. But, in order to support researchers using Windows based
operating systems the decision was made to leverage Docker virtualisation.

Docker provides a light-weight virtualisation layer enabling Linux software to
run on Windows with (relative) ease. It also has the added benefit of providing
a cloud based mechanism for disseminating software "images" to users. The advantage
of Docker over other systems, like VirtualBox or VMWare, are:

 * cloud based distribution of prebuilt images,
 * future releases will allow native Docker containers, and
 * easy to replicate virtual image creation.

### Why Python?

Python is a powerful and expressive scripting language. It comes with many
diverse packages, and has excellent support from developers (for example,
`fasStructure` is written in Python).


## Dependencies

When installing on any platform there are number of requisite dependencies:

 * Python
 * Docker

If you happen to be installing on Windows, then there are a couple of extra requirements:

 * Visual Studio Python compiler
 * MsysGit


## Installation

Begin by installing all of the dependencies for your operating system as
listed above.

Once complete, open a system terminal (please see the subsection on system terminals
below, under `usage`).

From an open system terminal, install the LAA Python interface with:

```bash
pip install laa
```

Next, from a system terminal, download and prepare the `laa` docker image. This
image contains `plink`, `fastStructure`, and the conversion scripts, all built
into a light-weight Alpine linux image:

```bash
laa init
```


## Usage

Usage is currently done directly from your operating system terminal. In Linux
like operating systems (including Mac OS X) use the system terminal emulator. In
Windows operating systems use the DOS prompt, which is typically accessible via
the `cmd.exe` command from the "run command" box.

Change directory to the location of your Excel data, and then run, for example:

```
laa all input.csv --maxk=5
```

To get help on command-line options, run:

```
laa --help
```
