# Semi Supervised Learning

### Example of applying expectation maximization to loss function := labeled_loss + unlabeled_loss

### Follows Nigam et al 2006 from "Semi-Supervised Learning", Chapelle et al.

## Running an experiment:

# python -m venv venv4ssl
# Windows/Anaconda: venv4ssl/Script/activate
# macos/Linux: source venv4ssl/bin/activate

# install our package
$ pip install ./SemiSupervisedLearning

# https://www.nltk.org/data.html

$ python src/download_nltk_data.py
$ python src/run_experiments.py
