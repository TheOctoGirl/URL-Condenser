import mariadb

try:
    import config
    if config.db_host == "DB_HOST_HERE":
        print("Please edit config.py and change the database credentials.")
        quit(1)

except ImportError:
    print("Please create a config.py file with your database credentials.")
    print("See default_config.py for an example.")
    quit(1)

class url_db:
    def connect():
        db = mariadb.connect(
            user=config.db_user,
            password=config.db_pass,
            host=config.db_host,
            port=config.db_port,
            database=config.db_name
        )
        cur = db.cursor()
        return db, cur
    
    def get_long_url(short_url :str):
        db, cur = url_db.connect()
        cur.execute("SELECT long_url FROM urls WHERE short_url=?", (short_url,))
        long_url = cur.fetchone()
        db.close()
        
        if long_url != None:
            return long_url[0]
        
        else:
            raise URLNotFoundError

    def get_short_url(long_url :str):
        db, cur = url_db.connect()
        cur.execute("SELECT short_url FROM urls WHERE long_url=?", (long_url,))
        short_url = cur.fetchone()
        db.close()
        
        if short_url != None:
            return short_url[0]

        else:
            raise URLNotFoundError

    def add_url(short_url :str, long_url :str):
        db, cur = url_db.connect()
        cur.execute("INSERT INTO urls (short_url, long_url) VALUES (?, ?)", (short_url, long_url))
        db.commit()
        db.close()
    
class URLNotFoundError(Exception):
    pass