# Semi Supervised Learning

### Example of applying expectation maximization to loss function := labeled_loss + unlabeled_loss
#### Dataset is "20 Newsgroups"

### Follows Nigam et al 2006 from "Semi-Supervised Learning", Chapelle et al.

## Running experiments:
```bash
$ python setup.py install
```

### nltk requirements
nltk >= 3.6

and

```nltk.corpus.stopwords```
which can be downloaded via

```bash
$ python -m nltk.downloader stopwords
```

Reference: [installing nltk data](https://www.nltk.org/data.html#installing-nltk-data)

### Run experiments when using number of labeled samples: 100,300,500,700,1000
```bash
$ python src/run_experiments_main.py 
--n_labeled 100,300,500,700,1000 
--n_unlabeled 10000 
--max_iters 10 
--out_dir <your_dir> 
--test_acc_plot_fname test_acc.png
```
<img src="https://user-images.githubusercontent.com/7552335/150062562-64e3c1fe-3f08-4dac-80c5-b9eb13e5c4fc.png" width="350" height="300" />

