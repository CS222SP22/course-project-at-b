# Introduction

## What is the assignment aggregator?

Tool for student to automatically track assignments from various LMSs
Script collects links to each LMS, and every night:
1. Checks the LMS for changed/new assignments
2. Adds them to a CSV
3. Outputs to user’s desired organizational software (Notion, Todoist)

# Technical Architecture



# Developers

- **Pranav Chandra**: Managing CSVs and Prairielearn WebScraping
- **Aniket Gargya**: Worked on Notion API implementation and LMS Class Template Importation
- **Liza George**: Worked on ToDoList API implementation and manging CSV debugging
- **Aydan Pirani**: Worked on Cron Jobs and Prairielearn Webscraping

# Environment Setup

## Initial venv Installation

Navigate to your source directory, and run the following command.

```
python3 -m venv ./venv
```

## Running venv

Before running any code, run the following:

```
venv/Scripts/activate/
```

# Development


## Package Updates

To enable package updates, run the following command ONCE: 
```
pip install pipreqs
```

To update packages, run the following from the home directory:
```
pipreqs . --force
```

## Package Management

To install packages, run the following:

```
pip install -r requirements.txt
```

# Project Instructions

1. To configure Notion for later reading:
```
python src/ics.py configure notion <database_id> <api_key>
```

Note, you must create:
- an integration. Use its "Internal Integration Token" as the `api_key`.
- a new database page, and clear all rows & columns (except the name column). Use this page's id as the `database_id`.

Detailed instructions on obtaining these parameters can be found here: https://developers.notion.com/docs/getting-started.

2. To add links for LMS:
```
python src/ics.py add <link> <lms>
```

3. To read and get your data:
```
python src/ics.py read [notion | todoist]
```
 - To access your assignments into Todoist, follow the instructions [here](https://todoist.com/help/articles/importing-or-exporting-project-templates#importing-project-templates-from-a-csv-file) to import the "new_data.csv" file to a Project. You can repeatedly import this file as it updates and Todoist will automatically merge them for you.
