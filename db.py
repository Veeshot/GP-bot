from replit import db
#file used to control database
for i in db.keys():
    if i == "messages":
        print("--------")
        print("{0} - {1}".format(i, db[i]))
        
    else:
        print("{0} - {1}".format(i, list(db[i])))
#launch přes konzoli - *python db.py*
#případě, že bot přestane běžet, protože ho discord zablokoval -> *kill 1* do konzole