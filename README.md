<div align="center">
  <img src="matt-artz-353291-unsplash.jpg" alt="Scissors">
</div>

# German Lemmatizer

A Python package (using a Docker image under the hood) to [lemmatize](https://en.wikipedia.org/wiki/Lemmatisation) German texts.

Built upon:

-   [IWNLP](https://github.com/Liebeck/spacy-iwnlp) uses the crowd-generated token tables on [de.wikitionary](https://de.wiktionary.org/).
-   [GermaLemma](https://github.com/WZBSocialScienceCenter/germalemma): Looks up lemmas in the [TIGER Corpus](http://www.ims.uni-stuttgart.de/forschung/ressourcen/korpora/TIGERCorpus/) and uses [Pattern](https://www.clips.uantwerpen.be/pattern) as a fallback for some rule-based lemmatizations.

It works as follows. First [spaCy](https://spacy.io/) tags the token with POS. Then `German Lemmatizer` looks up lemmas on IWNLP and GermanLemma. If they disagree, choose the one from IWNLP. If they agree or only one tool finds it, take it. Try to preserve the casing of the original token.

You may want to use underlying Docker image: [german-lemmatizer-docker](https://github.com/jfilter/german-lemmatizer-docker)

## Installation

1. Install [Docker](https://docs.docker.com/).
2. `pip install german-lemmatizer`

## Usage

1. Read and accept the [license terms of the TIGER Corpus](http://www.ims.uni-stuttgart.de/forschung/ressourcen/korpora/TIGERCorpus/license/htmlicense.html) (free to use for non-commercial purposes).
2. Make sure the Docker daemons runs.
3. Write some Python code

```python
from german_lemmatizer import lemmatize

lemmatize(
    ['Johannes war ein guter Schüler', 'Sabiene sang zahlreiche Lieder'],
    working_dir='*',
    chunk_size=10000,
    n_jobs=1,
    escape=False,
    remove_stop=False)
```

The list of texts is split into chunks (`chunk_size`) and processed in parallel (`n_jobs`).

Enable the `escape` parameter if your text contains newslines. `remove_stop` removes stopwords as defined by spaCy.

## License

MIT.
