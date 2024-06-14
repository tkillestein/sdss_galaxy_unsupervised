# How to get started
Below I've written a full set of instructions to start the repos


* Open the terminal

Setup
* `source /opt/miniconda3/bin/activate`
* `conda activate python39-env`
* `git clone https://github.com/tkillestein/sdss_galaxy_unsupervised`
* `cd sdss_galaxy_unsupervised`
* `mkdir data`
* `mv final_28x28_unproc.tar data`
* `cd data`
* `tar xvf final_28x28_unproc.tar` (go have a coffee for this step! )
* `cd ../`
* `python preproc_data.py`

Now run `jupyter lab` and a browser window will open for the exercises.

Now every time you want to work on the course, from a fresh terminal run:
* `source /opt/miniconda3/bin/activate`
* `conda activate python39-env`
* `jupyter lab`

When you're done, remember to hit `Ctrl-C` in the terminal, and follow the instructions to close the Jupyter server.