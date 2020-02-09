import numpy as np
import pandas as pd
from os import path
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
import matplotlib.font_manager
from src.analytics import *


def plot_word_cloud(text: str, max_font_size: int = 250, max_words: int = 250, background_color="white",
                    stopwords=None, width=2000, height=1500, case_sensitive: bool = False,
                    mask_path: str = None, caption: str = None):
    if stopwords is None:
        stopwords = []
    if mask_path is None:
        mask = mask_path
    else:
        mask = np.array(Image.open(mask_path))
        mask = transform_mask(mask)
    if not case_sensitive:
        text = text.lower()
    word_cloud = WordCloud(max_font_size=max_font_size, max_words=max_words, background_color=background_color,
                           stopwords=stopwords, width=width, height=height, mask=mask).generate(text)
    plt.imshow(word_cloud, interpolation="bilinear")
    plt.axis("off")
    if caption is not None:
        plt.suptitle(caption, fontsize=14, fontweight='bold')
    return plt.figure()


def transform_format(val):
    if 0 in val or all(v == 255 for v in val):
        return 255
    else:
        return 1


def transform_mask(mask):
    transformed_mask = np.ndarray((mask.shape[0], mask.shape[1]), np.int32)
    for i in range(len(mask)):
        transformed_mask[i] = list(map(transform_format, mask[i]))
    return transformed_mask


def plot_barh_dict(given_dict: dict, caption: str = None):
    plt.barh(range(len(given_dict)), given_dict.values(), align="center")
    plt.yticks(range(len(given_dict)), list(given_dict.keys()))
    plt.gca().invert_yaxis()
    if caption is not None:
        plt.suptitle(caption, fontsize=14, fontweight='bold')
    return plt.figure()


def plot_barv_dict(given_dict: dict, caption: str = None, xtick_number: int = None):
    if xtick_number is None:
        xtick_step = 1
    else:
        xtick_step = int(len(given_dict)/xtick_number)
    plt.bar(range(len(given_dict)), given_dict.values(), align="center")
    plt.xticks(range(0, len(given_dict), xtick_step), list(given_dict.keys())[0::xtick_step])
    if caption is not None:
        plt.suptitle(caption, fontsize=14, fontweight='bold')
    return plt.figure()


def plot_pie_chart(data: dict, caption: str = None, sort: bool = True):
    if sort:
        data = {k: v for k, v in sorted(data.items(), key=lambda item: item[1])}
    plt.pie(x=data.values(), labels=data.keys(), autopct="%1.2f%%", startangle=90)
    if caption is not None:
        plt.suptitle(caption, fontsize=14, fontweight='bold')
    return plt.figure()
