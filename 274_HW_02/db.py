from sqlalchemy import create_engine
from sqlalchemy.orm  import sessionmaker

from MCPII.models import Base, BlogPost, Author, Tag
import MCPII.parser as p

class BlogDB:
    def __init__(self, url, base=Base):
        engine = create_engine(url)
        base.metadata.create_all(engine)
        session_db = sessionmaker(bind=engine)
        self.__session= session_db()

    @property
    def session(self):
        return self.__session

if __name__ == '__main__' :

    db_url = 'sqlite:///blogpost.sqllite'
    db = BlogDB(db_url)

    all_tags, list_letters, aut_list =p.MStart('https://geekbrains.ru', 'https://geekbrains.ru/posts?page=0')
    print(list_letters[0])
    writers = [Author(itm[0], itm[1]) for itm in aut_list]
    tags = [Tag(itm[1], itm[0]) for itm in all_tags]

    for l in list_letters:
        ltag = []
        for tag_inx in l[4]:
            ltag.append(tags[tag_inx])
        blogpost = BlogPost(l[0], l[1],l[2], writers[l[3]],  ltag)
        db.session.add(blogpost)
        db.session.commit()
    print("ALL!!!")










    #writers1 = [Author(f'name_a{itm}', f'url_a{itm}') for itm in range(41, 42)]
    # tags = [Tag(f'tag_{itm}') for itm in range(30)]
   # blogpost = BlogPost('title3', 'url15', writers1[0], 'data')

   # db.session.add(writers1)
   # db.session.commit()
# blogpost = [BlogPost(itm[0], itm[1], writers[0], 'data' , tags[0:5]) for itm in list_letters]  #(title, link, aut, ltag_txt))
  #  print(tags)
   # writers = [Author(f'name_a{itm}', f'url_a{itm}') for itm in range(10,40)]
    #tags = [Tag(f'tag_{itm}') for itm in range(30)]
    #blogpost =[BlogPost('title1','url1', writers[5], 'data', tags[0:5])]
    #pass
    #db.session.add(blogpost)
    #db.session.commit()
    #pass

    #print(1)
    #writers1 =[Author(f'name_a{itm}', f'url_a{itm}') for itm in range(41, 42)]
    #tags = [Tag(f'tag_{itm}') for itm in range(30)]
    #blogpost = BlogPost('title3', 'url15', writers1[0], 'data')

    #db.session.add(blogpost)
    #db.session.commit()
