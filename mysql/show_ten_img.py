import ImageDB
db=ImageDB.db()
db.init()
ten=db.select_ten()
for row in ten:
	db.raw_to_img(row[3]).show()
