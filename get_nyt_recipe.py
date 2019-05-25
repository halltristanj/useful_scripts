import requests
from bs4 import BeautifulSoup
import textwrap
import argparse

textwidth = 125

parser = argparse.ArgumentParser(description='Print out a NYT recipe.')
parser.add_argument('-u', help='The URL.', required=True)
args = vars(parser.parse_args())


def remove_fract(text):
    fraction = {8585: u'.0', 43056: u'.25', 43057: u'.5', 43058: u'.75', 43059: u'.0625', 43060: u'.125', 43061: u'.1875', 188: u'.25', 189: u'.5', 190: u'.75', 8528: u'.142857142857', 8529: u'.111111111111', 8531: u'.333333333333', 8532: u'.666666666667', 8533: u'.2', 8534: u'.4', 8535: u'.6', 8536: u'.8', 8537: u'.166666666667', 8538: u'.833333333333', 8539: u'.125', 8540: u'.375', 8541: u'.625', 8542: u'.875', 69245: u'.333333333333', 3443: u'.25', 3444: u'.5', 3445: u'.75', 69243: u'.5', 69244: u'.25', 11517: u'.5', 69246: u'.666666666667'}
    text = text.translate(fraction)
    parts = map(float, text.split())
    return parts


print('\n\n\n')

# url = 'https://cooking.nytimes.com/recipes/1012494-spinach-tofu-and-sesame-stir-fry'
url = args['u']

r = requests.get(url)

soup = BeautifulSoup(r.text, 'html.parser')

ingredients = soup.find('section', attrs={'class': 'recipe-ingredients-wrap'})
recipe_steps = soup.find('ol', attrs={'itemprop': 'recipeInstructions'})

ingredients = ingredients.find_all('li', attrs={'itemprop': 'recipeIngredient'})
recipe_steps = recipe_steps.find_all('li')

print('*********** Ingredients *********************************')
for ingredient in ingredients:
    quantity = ingredient.find('span', attrs={'class': 'quantity'}).text.strip()
    ingred = ingredient.find('span', attrs={'class': 'ingredient-name'}).text.strip()
    if quantity:
        try:
            quantity = str(list(remove_fract(quantity))[0]).rstrip('0').rstrip('.')
        except ValueError:
            pass
        text = '- {0:>4} {1}'.format(quantity, ingred)
    else:
        text = '-      {}'.format(ingred)
    text = textwrap.wrap(text, width=textwidth)
    print(text[0])
    text.pop(0)
    for t in text:
        t = '    {}'.format(t)
        print(t)
print('*********************************************************\n')


print('*********** Directions **********************************')
n = 1
for step in recipe_steps:
    # Separate step by period
    sentences = step.text.split('.')

    print('  {}.'.format(n))
    print('- {}.'.format(sentences[0]))
    sentences.pop(0)
    for sentence in sentences:
        text = textwrap.wrap(sentence, width=textwidth)
        for t in text:
            print('- {}.'.format(t.strip()))

    n = n + 1

print('\n\n\n')
