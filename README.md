# Research Dataset Template

## Boilerplate and Guide for Future Datasets

> relies on [sscutils](https://github.com/sscu-budapest/sscutils) and the [tooling](https://sscu-budapest.github.io/tooling) of sscub

## To Create a New Dataset

### 1. Add Complete Dataset with Metadata

#### 1.1 Lay Out Structure

- if you need external namespaces, define them in `metadata/imported-namespaces.yaml`
  - `prefix: {uri: ..., tag (optional): ...}` format in yaml
  - import them to code with `inv import-namespaces`
- in-script metadata in `src/namespace_metadata.py`


#### 1.2 Adding Data

- load all the data to `complete` subset with the `update_data` function in `src/update_data.py`
- use ScruTable objects created in `namespace_metadata` to dump the data in `data` directory
- execute it with `inv update-data`
  - this calls the function defined in teh first step

#### 1.3 Add/Refine Metadata

- run `inv serialize-inscript-metadata` to move the structure defined in the script to `.yaml` files
- optionally extend the schema with descriptions where necessary

metadata schema is created with the intention for export to
- [(Postgre)SQL CREATE TABLE](https://www.postgresql.org/docs/current/sql-createtable.html)
- [W3 Tabular Metadata Standards](https://www.w3.org/TR/tabular-metadata/)

### 2. Configure DVC with Remotes

- add all remotes to main branch
- set default remotes for different branches with
  - fill `conf/default-remotes.yaml`
  - run `inv set-dvc-remotes`

### 3. Configure, Create and Push Environments

- create and document different environments with different access restrictions (in different dvc remotes)
  - save them to `conf/created-envs.yaml` using the `{name: {branch: ..., kwargs: {...}}` schema
  - either anonymized datasets with the same schema or simply smaller samples for personal workstation use


## To Update a dataset

- run the script that updates the `complete` subset
- run the commands creating and uploading the other subsets
  - `inv write-envs`
  - `inv push-envs --git-push`

## WIP: Basic Presentation of Dataset 

some script should present the dataset automatically

- schema diagram
- maybe some table profiling
- simple figures
- as general as possible
- with specifications regarding privacy / security
