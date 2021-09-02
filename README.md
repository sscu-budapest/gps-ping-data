# Research Dataset Template

## Boilerplate and Guide for Future Datasets

> relies on [sscutils](https://github.com/sscu-budapest/sscutils) and the [tooling](https://sscu-budapest.github.io/tooling) of sscub

### To create a new dataset

- setup storage for the data with dvc
- add metadata
- create and document different subsets with different access restrictions (in different dvc remotes)
  - either anonymized subsets or simply smaller samples for personal workstation use