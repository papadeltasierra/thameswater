# How to contribute

You're very welcome to make bug fixes or enhancements to this application. This
document lays out the guidelines for how to get those changes into the main
package repository.
 
## Getting Started
 
1. Fork the repository from github
```git
git clone git@github.com:papadeltasierra/thameswater.git
```
2. Make a branch off of master with a suitably descriptive name for your changes
```git
git checkout -b <branch_name>
```
3. You're now able to do work on this new branch

## Using your changes before they're live

You may want to use the changes you've made to this library before the merging/review
process has been completed. To do this you can install it into the global python 
environment by running this command from the top level directory.
```
pip install . --upgrade
```

## Submitting your changes

The master branch on this repository is protected so that only certain
DevOps folks can push directly to master or complete a merge request. This is
to demonstrate the following workflow for getting changes submitted.

1. Push your branch to github
```git
git push origin <branch_name>
```
2. Create a [merge request](https://github.com/add-merge-request.html)
on github. _Note that you're starting at step 2 in that document._
3. Assign the merge request to the project maintainer as detailed in the
central Metacom doc. They are responsible for reviewing your changes and will
work with you to get the changes released.