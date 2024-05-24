# Folder Synchronization Tool
___

## Table of Contents

1. [Overview](#overview)
1. [Features](#features)
1. [Environment](#environment)
1. [Installation](#installation)
1. [Usage](#usage)

## Overview
___

This project is a command-line tool for __synchronizing files__ from a __source directory__ to a __replica directory__ at regular intervals. 
It ensures that any changes in the source directory are mirrored in the replica directory. The tool also maintains logs of its 
operations, providing detailed information on the synchronization process.

## Features
___

1. One-way synchronization from __source__ to __replica__ directory 
1. Configurable synchronization interval
1. Logging of all synchronization activities
1. Automatic creation and deletion of files and directories in the __replica__ to match the __source__

## Environment
___

Python 3.7+

## Installation
___

- Clone the repository:
    
    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```


## Usage:

- For Help and Parameters description, execute the following command:

    ```sh
    python sync.py [-h] <source> <replica> [-i <interval>] [-lf <log_file>]
    ```

- Example:

    ```sh
    python sync.py /path/to/source /path/to/replica -i 3 -lf /path/to/logs/sync.log
    ```
