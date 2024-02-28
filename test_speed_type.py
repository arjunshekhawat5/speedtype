from speed_type import get_sentence, get_range, create_words_file
import os

def test_create_words_file():
    os.remove("words.txt")
    create_words_file()
    assert os.path.isfile("words.txt")

def test_get_sentence_easy():
    if not os.path.isfile("words.txt"):
        create_words_file()

    sentence = get_sentence()
    assert len(sentence.split()) > 2
    assert len(sentence.split()) < 7

def test_get_sentence_medium():
    if not os.path.isfile("words.txt"):
        create_words_file()

    sentence = get_sentence("medium")
    assert len(sentence.split()) > 6 
    assert len(sentence.split()) < 13
    

def test_get_sentence_hard():
    if not os.path.isfile("words.txt"):
        create_words_file()

    sentence = get_sentence("hard")
    assert len(sentence.split()) > 12
    assert len(sentence.split()) < 19
    

def test_get_sentence_insane():
    if not os.path.isfile("words.txt"):
        create_words_file()

    sentence = get_sentence("insane")
    assert len(sentence.split()) > 17
    assert len(sentence.split()) < 25
    

def test_get_range():
    easy_range = get_range("easy")
    assert easy_range == (3, 6)

    medium_range = get_range("medium")
    assert medium_range == (7, 12)
    
    hard_range = get_range("hard")
    assert hard_range == (13, 18)

    insane_range = get_range("insane")
    assert insane_range == (18, 24)
