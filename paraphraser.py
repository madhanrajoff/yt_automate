from parrot import Parrot
import torch
import warnings

from unittest import TestCase
from random import choice

warnings.filterwarnings("ignore")


class Paraphraser:
    def __init__(self, phrase=None, mark_question=False):
        # Init models (make sure you init ONLY once if you integrate this to your code)
        if phrase is None:
            phrase = 'Can you recommend some upscale restaurants in Newyork?'

        self.random_state(1234)  # to get reproducable paraphrase generations
        self.parrot = Parrot(model_tag="prithivida/parrot_paraphraser_on_T5")

        self.mark_question = mark_question
        self.phrase = self.cleansing(phrase)

    @staticmethod
    # uncomment to get reproducable paraphrase generations
    def random_state(seed):
        torch.manual_seed(seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(seed)

    def cleansing(self, sentence):
        unwanted = ['-', '.mp4']
        for ch in unwanted:
            if ch in sentence:
                sentence = sentence.split(ch)
                sentence = ' '.join(filter(lambda c: c.isalpha(), sentence))
            if self.mark_question and '?' not in sentence:
                sentence += '?'
        return sentence

    def rephrase(self):
        phrases = []
        print("-" * 100)
        print("Input_phrase: ", self.phrase)
        print("-" * 100)
        para_phrases = self.parrot.augment(input_phrase=self.phrase, use_gpu=False)
        for para_phrase in para_phrases:
            print(para_phrase)
            ph = para_phrase[0]
            ph = ph[:-1] if self.mark_question and ph.endswith('?') else ph
            if ph not in phrases:
                phrases.append(ph)
        return choice(phrases)


class ParaphraserTest(TestCase):

    def setUp(self):
        self.paraphraser = Paraphraser('droplets of water  on  a  calm  surface  of  water  in a  basin')

    def test_rephrase(self):
        phrases = self.paraphraser.rephrase()
        print(phrases)
