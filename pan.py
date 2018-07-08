#! /usr/bin/env python

import sys
import argparse

def sanitize_ingredient(ingredient):
    return ingredient.strip() ##.lower()

def parse_config_file(config_file_path):

    recipe = dict()

    for line in open(config_file_path).read().split('\n'):

        if not line or line.startswith('#'): # allow comments
            continue

        try:
            if ':' in line:
                ingredient, percentage = line.split(':')
            elif '=' in line:
                ingredient, percentage = line.split('=')

            ingredient = sanitize_ingredient(ingredient)
            percentage = float(percentage.strip())

            if ingredient in recipe:
                print('Skipping duplicated ingredient: %s.')
                continue

            recipe[ingredient] = percentage

        except:
            print('Skipping invalid line: %s.')
            continue

    return recipe


def get_total_percentage(recipe):
    total = 0.
    for ing, per in recipe.items():
        if ing == 'TZ':
            continue
        total += per

    return total


def get_ingredients_column_width(recipe):

    return width


parser = argparse.ArgumentParser(description='Pan calculations')

parser.add_argument('-t', dest='total', type=float, help='Total weight [g]')
parser.add_argument('-f', dest='flour', type=float, help='Flour weight [g]')

parser.add_argument('--fw', type=float, help='Water fraction')
parser.add_argument('--fs', type=float, help='Salt fraction')
parser.add_argument('--fy', type=float, help='Yeast fraction')
parser.add_argument('--fx', type=float, help='Sourdough fraction')

parser.add_argument('-x', '--sourdough', action='store_true', help='Use sourdough instead of yeast (assuming 100%% hidratation)')

parser.add_argument('-c', '--config', dest='config_file', help='Read percentages from config file')


args = parser.parse_args()

if args.total is None and args.flour is None:
    parser.print_help()
    sys.exit(1)


# Normal bread (using command line arguments)
if args.config_file is None:

    f_w  = 0.70  if args.fw is None else args.fw # water fraction
    f_s  = 0.02  if args.fs is None else args.fs # salt fraction
    f_y  = 0.002 if args.fy is None else args.fy # yeast fraction
    f_x  = 0.20  if args.fx is None else args.fx #

    w_f = 0 # flour weight
    w_w = 0 # water weight
    w_s = 0 # salt weight
    w_y = 0 # yeast weight
    w_x = 0

    if args.sourdough:
        if args.total:
            # calc flour weight
            w_t = args.total
            w_f = w_t / (1 + f_w + f_s)

        elif args.flour:
            w_f = args.flour
            w_t = w_f * (1 + f_w + f_s)


        w_x = w_f * f_x
        w_w = w_f * f_w
        w_s = w_f * f_s

        w_f -= 0.5*w_x # assuming 100% sourdough
        w_w -= 0.5*w_x

        output = """
Bread
=====
* Flour      = %7.2fg
* Water      = %7.2fg (%5.2f%%)
* Salt       = %7.2fg (%5.2f%%)
* Sourdough  = %7.2fg (%5.2f%%)

Total weight = %7.2fg
""" % (w_f, w_w, f_w*100, w_s, f_s*100, w_x, f_x*100, w_t)

    else:
        if args.total:
            # calc flour weight
            w_t = args.total
            w_f = w_t / (1 + f_w + f_s + f_y)

        elif args.flour:
            w_f = args.flour
            w_t = w_f * (1 + f_w + f_s + f_y)

        w_w = w_f * f_w
        w_s = w_f * f_s
        w_y = w_f * f_y

        output = """
Bread
=====
* Flour      = %7.2fg
* Water      = %7.2fg (%5.2f%%)
* Salt       = %7.2fg (%5.2f%%)
* Yeast      = %7.2fg (%5.2f%%)

Total weight = %7.2fg
""" % (w_f, w_w, f_w*100, w_s, f_s*100, w_y, f_y*100, w_t)

    print(output)


# Custom recipe (from config file)
if args.config_file is not None:

    w_t = args.total

    recipe = parse_config_file(args.config_file)

    total_percentage = get_total_percentage(recipe)

    # Calc recipe
    final_recipe = dict()
    total_weight = 0.
    for ing, per in recipe.items():

        w = per * (w_t / total_percentage)
        if ing != 'TZ':
            total_weight += w

        final_recipe[ing] = w



    # Print recipe
    print('Using configfile {0} for total weight = {1}\n'.format(args.config_file, args.total))


    # Fix

    print('+---------------------------------+')
    for ing, w in final_recipe.items():

        if 'TZ' in recipe:
            if ing == 'Harina':
                w -= final_recipe['TZ']
            elif ing == 'Agua':
                w -= (final_recipe['TZ']*5)
            elif ing == 'Leche':
                w -= (final_recipe['TZ']*5)

        if ing == 'TZ':
            w_s = '{%.0f/%.0f}' % (w, w*5)
        elif w < 1:
            w_s = '{0:.1f}'.format(w)
        else:
            w_s = '{0:.0f}'.format(w)



        print('|{0:<20} | {1:>10}|'.format(ing, w_s))

    print('+---------------------------------+')
    print('|{0:<20} | {1:>10.1f}|'.format('Total weight',  total_weight))
    print('+---------------------------------+')
