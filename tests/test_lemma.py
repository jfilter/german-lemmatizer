import os
import pathlib
import shutil

import pytest

import german_lemmatizer


def test_lemma():
    res = german_lemmatizer.lemmatize(["Johannes war einer von vielen guten Schülern."])
    assert list(res) == ["Johannes sein einer von vielen gut Schüler."]


def test_lemma_mass():
    res = german_lemmatizer.lemmatize(
        ["Johannes war einer von vielen guten Schülern."] * 1000,
        chunk_size=400,
        n_jobs=2,
    )
    assert list(res) == ["Johannes sein einer von vielen gut Schüler."] * 1000


def test_lemma_escape():
    res = german_lemmatizer.lemmatize(
        [
            "Johannes war einer von vielen guten Schülern.",
            """Peter war ein


        Idiot.""",
        ],
        escape=True,
    )
    assert list(res) == [
        "Johannes sein einer von vielen gut Schüler.",
        """Peter sein ein


        Idiot.""",
    ]
