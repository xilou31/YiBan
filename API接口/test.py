from model import *


def users(count=100):
    fake = Faker('zh_CN')
    i = 0
    while i < count:
        u = User(username=fake.user_name(),
                 nickname=fake.name(),
                 pwd='password',
                 email=fake.email(),
                 phone=fake.phone_number(),
                 school='scau')
        db.session.add(u)
        try:
            db.session.commit()
            i += 1
        except:
            db.session.rollback()


def blogs(count=100):
    fake = Faker('zh_CN')
    i = 0
    while i < count:
        b = Blog(title=

                 fake.sentence(nb_words=6, variable_nb_words=True, ext_word_list=None),
                 content=fake.text(),
                 user_id=i+1,
                 num_of_view=123,
                 face=fake.unix_device(prefix=None),
                 )

        db.session.add(b)
        try:
            db.session.commit()
            i += 1
        except:
            print("E")
            db.session.rollback()

def compet(count=100):
    fake = Faker('zh_CN')
    i = 0
    while i < count:
        c = Competition(title=

                        fake.sentence(nb_words=6, variable_nb_words=True, ext_word_list=None),
                        content=fake.text(),
                        author=fake.name(),
                        num_of_view=fake.ean(length=8)

                        )

        db.session.add(c)
        try:
            db.session.commit()
            i += 1
        except:
            db.session.rollback()


def acti(count=100):
    fake = Faker('zh_CN')
    i = 0
    while i < count:
        c = Activity(title=

                     fake.sentence(nb_words=6, variable_nb_words=True, ext_word_list=None),
                        content=fake.text(),
                        author=fake.name(),
                        num_of_view=fake.ean8()
                        )

        db.session.add(c)
        try:
            db.session.commit()
            i += 1
        except:
            print("e")
            db.session.rollback()

# users()
# compet()
# compet()
# acti()
# acti()
blogs()