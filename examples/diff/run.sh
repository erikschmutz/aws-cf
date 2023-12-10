CURRENT_DIR=$(dirname "$0")

python3 -m aws_cf diff -p $CURRENT_DIR/services.yml -r $CURRENT_DIR --verbose 1