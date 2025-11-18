rsync \
    -av \
    --exclude '.venv/' \
    --exclude '.venv/*' \
    --exclude '__pycache__/' \
    --exclude '__pycache__/*' \
    --exclude '.git/' \
    . di@hidpi.local:/home/di/autoyak