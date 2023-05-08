BACKUPS=/tmp/backups
rm -rf $BACKUPS
python backup.py sample_dir $BACKUPS
tree --charset ascii $BACKUPS
