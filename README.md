# Structure of our replication package SANER_2021

<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
* [Phase1: DVC projects caracteristics](#phase1-dvc-projects-caracteristics)
* [Phase2: DVC coupling with source code artifacts](#phase2-dvc-coupling-with-source-code-artifacts)
  * [Description of coupling-statiscal test scripts](#description-of-coupling-statiscal-test-scripts)
  * [Commit-level analysis (25 projects)](#commit-level-analysis-25-projects)
    * [internal DVC categories coupling](#internal-dvc-categories-coupling)
    * [coupling with source code artifacts](#coupling-with-source-code-artifacts)
  * [Pull Request-level analysis (10 projects):](#pull-request-level-analysis-10-projects)
    * [internal DVC categories coupling](#internal-dvc-categories-coupling-1)
    * [coupling with source code artifacts](#coupling-with-source-code-artifacts-1)
* [Phase3: Complexity evolution of ML pipelines](#phase3-complexity-evolution-of-ml-pipelines)
  * [McCabe vs Halstead complexity](#halstead-vs-mccabe)
  * [McCabe complexity](#mccabe-complexity)
  * [Halstead complexity](#halstead-complexity)


## About The Project
Mining software repositories related to datasets and machine learning traceability

In the following package, we share a list of mined repository to study the co-evolution between the dvc ML and data tracking and the source code artifacts.
We classified the dvc features in three classes:
- DVC-data: DVC files that only track data
- DVC-pipeline: DVC files that track a pipeline, they are caracterised by the keywords ("cmd": for the executed command and "deps": for the stage dependencies) 
- DVC-utility: DVC files within the `.dvc` folder .i.e,.dvc/config, .dvc/gitignore.

This is how a DVC can be used inside a repository:

![pipeline_commands](https://user-images.githubusercontent.com/73168850/97630923-9c56eb00-1a06-11eb-941f-a0a42d1ea6b5.png)

We classified the source code artifacts in five categories (Source code, Test, Data, Gitignore, Others).

## Phase1: DVC projects caracteristics

In a first part of this study we analysed 391 projects that was gathered on the 28 Febrary 2020 from Github. We want to explore the usage of DVC in these repositories and their caracteristics.
The list of the repositories are listed in file <path of file>
* The following figure show the period these projects waited to start trying dvc (first day creating the repository until first day starting dvc)

![applying_dvc](https://user-images.githubusercontent.com/73168850/97631642-aa593b80-1a07-11eb-9612-b1abfa1d1696.png)


* The following figure show how long the projects has been using DVC since the first commit introducing a DVC file.

![usage](https://user-images.githubusercontent.com/73168850/97631577-91e92100-1a07-11eb-8f3d-c2ee664041fd.png)

The following figure show the remote storage used in these repositories.

![remote](https://user-images.githubusercontent.com/73168850/97631460-65cda000-1a07-11eb-944f-f9b54b901ce4.png)

* We plot the distribution of the DVC files changes by project commits chronologically in grouped chrunks of 10%.
<img src="https://user-images.githubusercontent.com/73168850/97632222-9a8e2700-1a08-11eb-8b90-e1f1f3d5e34c.png" width="500" height="400" />


## Phase2: DVC coupling with source code artifacts

In the second part of this study, we studied the coupling between different categories of dvc and source code artifacts at two levels:

### Description of coupling-statiscal test scripts

In the following we will present a sample of script that we used to compute the coupling between the "DVC pipeline category" and "source code artifacts(source, test, data, gitignore, others)":

* Step1: 
you have to download all the projects, we used in the analysis of the coupling in commit level mentioned in the file "Commit_projects.csv".

* Step2:
Provide the path of the repository where the projects were downloaded as argument <arg1>

* Step3:
Execute the script:
python3 coupled_commits.py <path_source_reposiotry>



We use a χ2 chi-squared statistical test to validate the statistical significance of the coupling between changes to A and B, for example (DVC-data and test).
We present in the following a script sample we used to compute the statistical significance between "dvc data category" and "source code artifacts(source, test, data, gitignore, others)".



* Step1: 
you have to download all the projects, we used in the analysis of the coupling in pull request level mentioned in the file "Pull_request_projects.csv".

* Step2:
Provide the path of the repository where the projects were downloaded as argument <arg1>

* Step3:
Execute the script:
python3 significance_pr.py <path_source_reposiotry>


The results of the coupling are shown in the following plots of the commit and pull request level analysis.

### Commit-level analysis (25 projects):
#### internal DVC categories coupling


<p float="left">
 <img src="https://user-images.githubusercontent.com/73168850/97638978-1772ce00-1a14-11eb-9344-aa5b2306fe8d.png" width="250" />
 <img src="https://user-images.githubusercontent.com/73168850/97638979-180b6480-1a14-11eb-80e2-6d3af4ddb603.png" width="250" />
 <img src="https://user-images.githubusercontent.com/73168850/97638981-180b6480-1a14-11eb-8b5f-0644d1203678.png" width="250" />
</p>

#### coupling with source code artifacts

<p float="left">
 <img src="https://user-images.githubusercontent.com/73168850/97638999-1e99dc00-1a14-11eb-8245-cb22d7ccd638.png" width="250" />
 <img src="https://user-images.githubusercontent.com/73168850/97639000-1e99dc00-1a14-11eb-8a51-dee5c05ca4f9.png" width="250" />
 <img src="https://user-images.githubusercontent.com/73168850/97639002-1e99dc00-1a14-11eb-8901-5f6c56331617.png" width="250" />
</p>

### Pull Request-level analysis (10 projects):
#### internal DVC categories coupling


<p float="left">
 <img src="https://user-images.githubusercontent.com/73168850/97639014-25c0ea00-1a14-11eb-8ed7-90b034623538.png" width="250" />
 <img src="https://user-images.githubusercontent.com/73168850/97639016-25c0ea00-1a14-11eb-8e58-9396dc8083aa.png" width="250" />
 <img src="https://user-images.githubusercontent.com/73168850/97639019-26598080-1a14-11eb-8ecc-5a9509837141.png" width="250" />
</p>

#### coupling with source code artifacts


<p float="left">
 <img src="https://user-images.githubusercontent.com/73168850/97638949-088c1b80-1a14-11eb-9363-6c113f020527.png" width="250" />
 <img src="https://user-images.githubusercontent.com/73168850/97638950-0924b200-1a14-11eb-8e91-f2e9f34c9a0e.png" width="250" />
 <img src="https://user-images.githubusercontent.com/73168850/97638951-0924b200-1a14-11eb-80e2-c0b8ff37575f.png" width="250" />
</p>

## Phase3: Complexity evolution of ML pipelines
In the Third part of this study, we studied the complexity evolution of the ML pipeline over time in a list of 25 projects
### Halstead vs McCabe 

<p float="left">
  <img src="https://user-images.githubusercontent.com/73168850/97633678-db873b00-1a0a-11eb-8544-95f271948997.png" width="500" />
</p>

### McCabe Complexity

<p float="left">
  <img src="https://user-images.githubusercontent.com/73168850/97635857-759cb280-1a0e-11eb-9545-cdf3b23fe0a9.png" width="500" />
</p>

<p float="left">
  <img src="https://user-images.githubusercontent.com/73168850/97634742-9e23ad00-1a0c-11eb-9f48-fa2cc5100b64.png" width="200" />
  <img src="https://user-images.githubusercontent.com/73168850/97634773-aa0f6f00-1a0c-11eb-9172-aa2935bf3be8.png" width="200" /> 
  <img src="https://user-images.githubusercontent.com/73168850/97635471-ce1f8000-1a0d-11eb-90e2-8513e3f8c010.png" width="200" /> 
  <img src="https://user-images.githubusercontent.com/73168850/97635484-d37cca80-1a0d-11eb-9628-12b74bc020d6.png" width="200" /> 
  <img src="https://user-images.githubusercontent.com/73168850/97635495-d5df2480-1a0d-11eb-8c5e-27eaaf833af4.png" width="200" /> 
  <img src="https://user-images.githubusercontent.com/73168850/97635497-d7a8e800-1a0d-11eb-9de4-171d3e8f33da.png" width="200" /> 
  <img src="https://user-images.githubusercontent.com/73168850/97635505-daa3d880-1a0d-11eb-974b-041248300d4f.png" width="200" /> 
  <img src="https://user-images.githubusercontent.com/73168850/97635510-dd063280-1a0d-11eb-86a3-b54d73d085e7.png" width="200" /> 
  <img src="https://user-images.githubusercontent.com/73168850/97635521-df688c80-1a0d-11eb-87c0-7a0896921890.png" width="200" /> 
  <img src="https://user-images.githubusercontent.com/73168850/97635529-e1cae680-1a0d-11eb-88fe-df1934441639.png" width="200" /> 
  <img src="https://user-images.githubusercontent.com/73168850/97635541-e4c5d700-1a0d-11eb-9a54-9684def6bf0c.png" width="200" /> 
  <img src="https://user-images.githubusercontent.com/73168850/97635546-e7283100-1a0d-11eb-8633-93c09803f74e.png" width="200" /> 
  <img src="https://user-images.githubusercontent.com/73168850/97635552-ea232180-1a0d-11eb-8819-51a3a3edff8a.png" width="200" /> 
  <img src="https://user-images.githubusercontent.com/73168850/97635565-ef806c00-1a0d-11eb-877d-1cc9a5aa6384.png" width="200" /> 
  <img src="https://user-images.githubusercontent.com/73168850/97635574-f1e2c600-1a0d-11eb-864b-58a5c06d93b1.png" width="200" /> 
  <img src="https://user-images.githubusercontent.com/73168850/97635581-f4452000-1a0d-11eb-95af-500cb46c57e2.png" width="200" /> 
  <img src="https://user-images.githubusercontent.com/73168850/97635589-f7401080-1a0d-11eb-82ec-4e33da293d5b.png" width="200" /> 
  <img src="https://user-images.githubusercontent.com/73168850/97635594-f9a26a80-1a0d-11eb-8aa8-f917777bbcf7.png" width="200" /> 
  <img src="https://user-images.githubusercontent.com/73168850/97636255-36bb2c80-1a0f-11eb-8c7b-8a8b52154463.png" width="200" /> 
  <img src="https://user-images.githubusercontent.com/73168850/97636258-39b61d00-1a0f-11eb-8f6c-e8a2ac9c9d14.png" width="200" /> 
  <img src="https://user-images.githubusercontent.com/73168850/97636264-3cb10d80-1a0f-11eb-8e0e-76b909987276.png" width="200" /> 
  <img src="https://user-images.githubusercontent.com/73168850/97636271-3e7ad100-1a0f-11eb-8ded-68aaba6be172.png" width="200" /> 
  <img src="https://user-images.githubusercontent.com/73168850/97636276-40dd2b00-1a0f-11eb-9d2b-82caa5e20e2f.png" width="200" /> 
  <img src="https://user-images.githubusercontent.com/73168850/97636278-433f8500-1a0f-11eb-8181-e131a926db2c.png" width="200" /> 
  <img src="https://user-images.githubusercontent.com/73168850/97636285-45a1df00-1a0f-11eb-9992-87360f2273d7.png" width="200" /> 
</p>


### Halstead Complexity

<p float="left">
  <img src="https://user-images.githubusercontent.com/73168850/97636810-088a1c80-1a10-11eb-83c7-364161a7eaca.png" width="500" />
</p>

<p float="left">
  <img src="https://user-images.githubusercontent.com/73168850/97637000-4d15b800-1a10-11eb-89f9-ea14e5042b53.png" width="200" />
  <img src="https://user-images.githubusercontent.com/73168850/97637001-4d15b800-1a10-11eb-80e3-4a112e4e5ff6.png" width="200" />
  <img src="https://user-images.githubusercontent.com/73168850/97637002-4d15b800-1a10-11eb-93bf-ba500926bef9.png" width="200" />
  <img src="https://user-images.githubusercontent.com/73168850/97637003-4d15b800-1a10-11eb-995f-fe531ad950ce.png" width="200" />
  <img src="https://user-images.githubusercontent.com/73168850/97637004-4d15b800-1a10-11eb-8969-c43ba23cd94d.png" width="200" />
  <img src="https://user-images.githubusercontent.com/73168850/97637005-4dae4e80-1a10-11eb-8c97-c61a444389a1.png" width="200" />
  <img src="https://user-images.githubusercontent.com/73168850/97637006-4dae4e80-1a10-11eb-94f2-ab9a9c9f2f2a.png" width="200" />
  <img src="https://user-images.githubusercontent.com/73168850/97637007-4dae4e80-1a10-11eb-982d-21e27abdfde0.png" width="200" />
  <img src="https://user-images.githubusercontent.com/73168850/97637008-4dae4e80-1a10-11eb-87db-c85885623eb4.png" width="200" />
  <img src="https://user-images.githubusercontent.com/73168850/97637009-4e46e500-1a10-11eb-88ee-b8aa6e012d13.png" width="200" />
  <img src="https://user-images.githubusercontent.com/73168850/97637010-4e46e500-1a10-11eb-8803-1f0d376efc64.png" width="200" />
  <img src="https://user-images.githubusercontent.com/73168850/97637011-4e46e500-1a10-11eb-8a80-5f2461a878d4.png" width="200" />
  <img src="https://user-images.githubusercontent.com/73168850/97637012-4e46e500-1a10-11eb-80da-e89ccc440847.png" width="200" />
  <img src="https://user-images.githubusercontent.com/73168850/97637014-4e46e500-1a10-11eb-985e-0d8d1326d7d9.png" width="200" />
  <img src="https://user-images.githubusercontent.com/73168850/97637015-4e46e500-1a10-11eb-9282-3cf3e6b0c1a6.png" width="200" />
  <img src="https://user-images.githubusercontent.com/73168850/97637016-4edf7b80-1a10-11eb-8287-58aa0aa7da28.png" width="200" />
  <img src="https://user-images.githubusercontent.com/73168850/97637017-4edf7b80-1a10-11eb-8367-4dcaaa7ee5fd.png" width="200" />
  <img src="https://user-images.githubusercontent.com/73168850/97637018-4edf7b80-1a10-11eb-9322-ac47da7bc206.png" width="200" />
  <img src="https://user-images.githubusercontent.com/73168850/97637019-4edf7b80-1a10-11eb-968d-55e759327364.png" width="200" />
  <img src="https://user-images.githubusercontent.com/73168850/97637020-4edf7b80-1a10-11eb-8d55-cc9e430649c7.png" width="200" />
  <img src="https://user-images.githubusercontent.com/73168850/97637021-4f781200-1a10-11eb-8de1-8f9c32f83215.png" width="200" />
  <img src="https://user-images.githubusercontent.com/73168850/97637022-4f781200-1a10-11eb-8ab9-0912ab002110.png" width="200" />
  <img src="https://user-images.githubusercontent.com/73168850/97637023-4f781200-1a10-11eb-96a7-7595aa1e27a5.png" width="200" />
  <img src="https://user-images.githubusercontent.com/73168850/97637024-4f781200-1a10-11eb-9691-e817d756c7b9.png" width="200" />
  <img src="https://user-images.githubusercontent.com/73168850/97637025-4f781200-1a10-11eb-9d44-bcf73ff92daf.png" width="200" />
  
</p>


