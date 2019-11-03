# PATV-Physical-Address-Translation-Viewer
2nd project for the 'Operating System' course.
Given a pid, this python program finds all the memory pages that this process has, and checks how many are in RAM or not, while also printing their page table entries and page frame number.

Further explanation and context can be found [here (in portuguese)](https://lasca.ic.unicamp.br/paulo/courses/so/2019s2/exp/exp03.html).

<!-- ## Getting Started

If you want to try  -->

### Prerequisites

You are going to need *Python 3* to run this code.

### How to run

First, clone this repository to your PC:

```
git clone https://github.com/danielferragut/PATV-Physical-Address-Translation-Viewer/
```

Change directories to the new *PATV-Physical-Address-Translation-Viewer* directory created.

To run, just type:
```
python3 patv.py [pid]
```
[pid] being the process id for the desired process. *Sudo* is necessary, otherwise the page frame number for pages in RAM is going to be 0x0.


<!-- ## Built With

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags).  -->

## Authors

* **Daniel Ferragut**
* **Lucas Koiti**
