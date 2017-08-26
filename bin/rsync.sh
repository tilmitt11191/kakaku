
SRC_DIR=/home/ozu/program/kakaku
DST_DIR=/home/cc1g/lib/
rsync -av --delete --exclude='.git' --include='*/' --include="*.sh" --include='*.py' --include='kakaku' --exclude='*' $SRC_DIR $DST_DIR
