# Research Dataset Template

## Boilerplate and Guide for Future Datasets

> relies on [sscutils](https://github.com/sscu-budapest/sscutils) and the [tooling](https://sscu-budapest.github.io/tooling) of sscub

## WIP Notes:

- subset to be renamed: current proposal to `env` short for environment
- configuration files moved to `conf` directory
- metadata files moved / *duplicated*
  - `src/trepos.py` and `src/raw_cols.py` might be merged, might be moved/renamed, referred to as "in-script metadata"
  - **proposal**: metadata files copied as yaml to `metadata` directory
  - possibly introduce some auto metadata detection/generation based on in-script metadata and parquet tables to sscutils to ease the process

## To Create a New Dataset

### 1. Add Complete Dataset with Metadata

#### 1.1 Lay Out Structure

- to in-script metadata

#### 1.2 Adding Data

load all the data to `complete` subset

#### 1.3 Add/Refine Metadata

stored in 3 places, that need to be kept in sync:
- in parquet files
  - `data/**.parquet`
- in config yamls
  - `metadata/*.yaml`
- in-script metadata
  - **currently** `raw_cols.py` and `trepos.py`

with the intention for export to
- [(Postgre)SQL CREATE TABLE](https://www.postgresql.org/docs/current/sql-createtable.html)
- [W3 Tabular Metadata Standards](https://www.w3.org/TR/tabular-metadata/)

so needs information about column types, column groups, foreign keys and indices, optionally descriptions and restrictions

### 2. Configure DVC with Remotes

- add all remotes to main branch
- set default remotes for different branches with
  - fill `conf/default-remotes.yaml`
  - run `inv set-dvc-remotes`

### 3. Configure, Create and Push Environments

- create and document different environments with different access restrictions (in different dvc remotes)
  - either anonymized datasets with the same schema or simply smaller samples for personal workstation use


## To Update a dataset

- run the script that updates the `complete` subset
- run the commands creating and uploading the other subsets
  - `inv write-dataset-envs`
  - `inv push-dataset-envs --git-push`

## WIP: Basic Presentation of Dataset 

some script should present the dataset automatically

- maybe some table profiling
- simple figures
- as general as possible
- with specifications regarding privacy / security
