import sys
import re
from tqdm import tqdm
from argparse import ArgumentParser
from collections import Counter

ALPHA_RATIO = 0.5
MIN_WORDS = 2

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--left', type=str, required=True)
    parser.add_argument('--right', type=str, required=True)
    parser.add_argument('--ignore_subset', type=str, default='')
    parser.add_argument('--filter', action='store_true')
    args = parser.parse_args()
    corpora = Counter()
    with open(args.left, 'at') as fid_l, open(args.right, 'at') as fid_r:
        for line in tqdm(sys.stdin):
            parts = line.split('\t')
            left, right = parts[0], parts[1]
            subset = parts[-1] if len(parts) == 3 else None

            valid_line = True
            if args.filter:
                if len(left) > 0:
                    ratio = sum(c.isalpha() for c in left) / len(left)
                    words_count = len(re.findall(r'[a-zA-ZäöüßÄÖÜ]+', left))
                    valid_line = ratio >= ALPHA_RATIO and words_count >= MIN_WORDS
                else:
                    valid_line = False
            if subset != args.ignore_subset and valid_line:
                fid_l.write(left.strip('\n') + '\n')
                fid_r.writelines(right.strip('\n') + '\n')
            corpora.update([subset])
    print('Processed corpora: {}'.format(corpora))
