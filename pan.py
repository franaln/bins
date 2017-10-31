import sys
import argparse

parser = argparse.ArgumentParser(description='Pan calculations')

parser.add_argument('-t', dest='total', type=float, help='Total weight [g]')
parser.add_argument('-f', dest='flour', type=float, help='Flour weight [g]')

parser.add_argument('--fw', type=float, help='Water fraction')
parser.add_argument('--fs', type=float, help='Salt fraction')
parser.add_argument('--fy', type=float, help='Yeast fraction')
parser.add_argument('--fx', type=float, help='Sourdough fraction')

parser.add_argument('-x', dest='sourdough', action='store_true', help='Use sourdough instead of yeast (assuming 100% hidratation)')

args = parser.parse_args()

if args.total is None and args.flour is None:
    parser.print_help()
    sys.exit(1)

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

        w_f = w_t / (1 + f_w + f_x + f_s)

    elif args.flour:

        w_f = args.flour

        w_t = w_f * (1 + f_w + f_x + f_s)


    w_x = w_f * f_x

    w_w = w_f * f_w
    w_s = w_f * f_s
    w_y = w_f * f_y

    w_f -= 0.5*w_x
    w_w -= 0.5*w_x

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


if args.sourdough:
    output = """
Bread
=====

* Flour    : %7.2fg
* Water    : %7.2fg (%5.2f%%)
* Salt     : %7.2fg (%5.2f%%)
* Sourdough: %7.2fg (%5.2f%%)

Total weight = %7.2fg
""" % (w_f, w_w, f_w*100, w_s, f_s*100, w_x, f_x*100, w_t)

else:
    output = """
Bread
=====

* Flour: %7.2fg
* Water: %7.2fg (%5.2f%%)
* Salt : %7.2fg (%5.2f%%)
* Yeast: %7.2fg (%5.2f%%)

Total weight = %7.2fg
""" % (w_f, w_w, f_w*100, w_s, f_s*100, w_y, f_y*100, w_t)

print(output)
