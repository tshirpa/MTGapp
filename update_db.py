#This needs to be ran before the application can run
from mtgtools.MtgDB import MtgDB
mtg_db = MtgDB('my_db.fs')
mtg_db.mtgio_update()