#!/bin/bash
pipenv run pyinstaller \
--add-data MTGcardback.jpg:./ \
--add-data read_from_image.py:./ \
--add-data ./mtg_cards_settings.py:./ \
--add-data ./update_db.py:./ \
--hidden-import cv2 \
--exclude-module IPython \
--paths ./ \
--clean --noconfirm --onefile \
mtg_app.py

pipenv run pyinstaller \
--exclude-module IPython \
--paths ./ \
--clean --noconfirm --onefile \
update_db.py
