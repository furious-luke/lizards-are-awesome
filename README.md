# lizards-are-awesome

A Docker based workflow for performing a Plink/fastStructure analysis from Excel data.


## Overview

This software seeks to ease much the manual labour involved in preparing data for
running with Plink and fasStructure. Most of the work, besides the mentioned
external packages, is done with a Python script. The primary operations
performed are:

 1. Duplicating the input data.
 2. Performing a substitution on certain values in the duplicated data.
 3. Indpenendantly indexing both sets of data.
 4. Combining the original and duplicated data.
 5. Sorting on the index.
 6. Transposing the combined data.
 7. Outputting to a Plink compatible format.

Whereas before these steps would be carred out manually using various software
packages, they are now performed automatically with one command.

In addition to the main conversion operation, there are additional functions
to perform analysis runs of Plink and fasStructre, passing the data files
between the two programs automatically.


## Design Decisions

### Why Docker?

`Plink` is written for Linux based operating systems. As such on a Linux system
all operations could be performed directly, without the need for any kind of
virtualisation layer. But, in order to support researchers using Windows based
operating systems the decision was made to leverage Docker virtualisation.

Docker provides a light-weight virtualisation layer enabling Linux software to
run on Windows with (relative) ease. It also has the added benefit of providing
a cloud based mechanism for disseminating software images to users. The advantage
of Docker over other systems, like VirtualBox or VMWare, are:

 * cloud based distribution of prebuilt images,
 * future releases will allow native Docker containers, and
 * easy to replicate virtual image creation.

### 


## External Packages

The Docker image utilises:

 * `Plink` package: http://pngu.mgh.harvard.edu/~purcell/plink/
 * fasStructure (link)


## Dependencies

When installing on any platform there are number of requisite dependencies:

 * Python
 * Fabric
 * Docker

If you happen to be installing on Windows, then there are a few extra requirements:

 * Visual Studio Python compiler
 * MsysGit


## Installation

Once all dependencies are installed, the Docker image must be retrieved
from the Docker Hub servers:

```bash
fab init
```

## Usage

Change directory to the location of your Excel data, and then run, for example:

```
fab all:input.xlsx,maxk=5
```
