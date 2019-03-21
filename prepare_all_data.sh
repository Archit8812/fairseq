#!/usr/bin/env bash

SOURCE_LANG=de
TARGET_LANG=en
BIN=data-bin/wmt18ensemble
BIN_OUT=data-bin/wmt18full

ROOT_DIR=examples/translation

TEXTDIR=$ROOT_DIR/translation/wmt17_de_en
TMP=$TEXTDIR/tmp

SCRIPTS=$ROOT_DIR/mosesdecoder/scripts
TOKENIZER=$SCRIPTS/tokenizer/tokenizer.perl
DETOKENIZER=$SCRIPTS/tokenizer/detokenizer.perl
CLEAN=$SCRIPTS/training/clean-corpus-n.perl
NORM_PUNC=$SCRIPTS/tokenizer/normalize-punctuation.perl
REM_NON_PRINT_CHAR=$SCRIPTS/tokenizer/remove-non-printing-char.perl
BPEROOT=$ROOT_DIR/subword-nmt/subword_nmt

BPE_CODE=$TEXTDIR/code

CORPORA_DIR=data-bin/corpora
TRANSLATIONS_DIR=$CORPORA_DIR/translations

for N in {0..104}
do
    echo "Processing shard $N"
    cat $TRANSLATIONS_DIR/translation.$N.output | grep -P '^S' | cut -f2- | sed 's/@@\s*//g' | \
        python $BPEROOT/apply_bpe.py -c $BPE_CODE >> $TMP/bpe.train.$TARGET_LANG
    cat $TRANSLATIONS_DIR/translation.$N.output | grep -P '^H' | cut -f3- | sed 's/@@\s*//g' | \
        python addnoise.py | python $BPEROOT/apply_bpe.py -c $BPE_CODE >> $TMP/bpe.train.$SOURCE_LANG
done
echo "Cleaning corpus"
perl $CLEAN -ratio 1.5 $TMP/bpe.train $SOURCE_LANG $TARGET_LANG $TEXTDIR/train 1 250