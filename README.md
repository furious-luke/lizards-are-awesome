# lizards-are-awesome

A Docker based workflow for performing a Plink/fastStructure analysis from Excel data.


## External Packages

Using the excellent `Plink` package: http://pngu.mgh.harvard.edu/~purcell/plink/


## Installation

Dependencies:

 * Docker
 * Python
 * Fabric

After installing the dependencies, pull the docker image:

```
docker pull furiousluke/laa:latest
```

## Usage

Change directory to the location of your Excel data, and then run, for example:

```
fab all:input.xlsx,maxk=5
```
