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
    parser.add_argument('--ignore_subset', type=str, default=None)
    args = parser.parse_args()
    corpora = Counter()
    with open(args.left, 'at') as fid_l, open(args.right, 'at') as fid_r:
        for line in tqdm(sys.stdin):
            left, right, subset = line.split('\t')

            ratio = sum(c.isalpha() for c in left) / len(left)
            words_count = len(re.findall(r'[a-zA-ZäöüßÄÖÜ]+', left))
            if subset != args.ignore_subset and ratio >= ALPHA_RATIO and words_count >= MIN_WORDS:
                fid_l.write(left + '\n')
                fid_r.writelines(right + '\n')
            corpora.update([subset])
    print('Processed corpora: {}'.format(corpora))