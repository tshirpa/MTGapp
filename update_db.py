#This needs to be ran before the application can run
from mtgtools.MtgDB import MtgDB
from pathlib import Path
db_path = Path("~/Documents/'my_db.fs'").expanduser()
db_path_str = str(db_path)
mtg_db = MtgDB(db_path_str)
mtg_db.mtgio_update()
