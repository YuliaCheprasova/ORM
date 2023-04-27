from peewee import *


conn = PostgresqlDatabase(user="postgres",
                            password="22424",
                            host="127.0.0.1",
                            port="5432",
                            database="db_for_work_with_python")


class exhibitions(Model):
    exhibition_id = AutoField(primary_key=True)
    name = CharField()
    duration = TimeField(null=True)
    age_limit = SmallIntegerField(null=True)

    class Meta:
        database=conn


class sessions(Model):
    session_id = AutoField(primary_key=True)
    date_of_session = DateField()
    time_of_session = TimeField()
    exhibition_id = ForeignKeyField(exhibitions, backref='sessions', to_field='exhibition_id', null=True)

    class Meta:
        database=conn


def exhibitions_show():
    print("\nTable exhibitions:\n")
    exhibitions_show = exhibitions.select().dicts().execute()
    for exhibition in exhibitions_show:
        print(exhibition)
    print("\n")


def sessions_show():
    print("\nTable sessions:\n")
    sessions_show = sessions.select().dicts().execute()
    for session in sessions_show:
        print(session)
    print("\n")


if __name__ == '__main__':

    with conn.cursor() as cursor:
        exhibitions.create_table()
        print("Table exhibitions is created")
        exhibitions_data = [{'name': 'The Pushkin', 'duration': '1:50','age_limit': 16},
        {'name':'Our_predecessors', 'duration': '2:30', 'age_limit': 12},
        {'name': 'The wonders of science', 'duration': '1:10', 'age_limit': 16},
        {'name': 'The World of animals',  'duration': '1:30', 'age_limit': 0}]
        exhibitions.insert_many(exhibitions_data).execute()
        print("Values are added in table exhibitions")
        exhibitions_show()
        update_q = exhibitions.update(age_limit=14).where(exhibitions.age_limit==16).execute()
        print("Table exhibitions is updated")
        exhibitions_show()
        delete_q = exhibitions.delete().where(exhibitions.name == 'The Pushkin').execute()
        print("Values are deleted from table exhibitions")
        exhibitions_show()
        sessions.create_table()
        print("Table sessions is created")
        sessions_data = [{'date_of_session': '2023-03-23', 'time_of_session': '18:00', 'exhibition_id': 4},
                         {'date_of_session':'2023-04-01', 'time_of_session': '21:30','exhibition_id': 4},
                         {'date_of_session':'2023-04-08', 'time_of_session':'19:00', 'exhibition_id':3},
                         {'date_of_session':'2023-04-11', 'time_of_session':'18:00', 'exhibition_id':2},
                         {'date_of_session':'2023-06-06', 'time_of_session':'13:00', 'exhibition_id':4},
                         {'date_of_session':'2023-03-29', 'time_of_session':'13:30', 'exhibition_id':4}]
        sessions.insert_many(sessions_data).execute()
        print("Values are added in table sessions")
        sessions_show()
        join_q = (exhibitions.select(exhibitions.name, sessions.date_of_session, sessions.time_of_session)
                  .join(sessions)
                  .where(exhibitions.name == 'The World of animals')).execute()
        for tuple in join_q:
            print(tuple.name, tuple.sessions.date_of_session, tuple.sessions.time_of_session)
        sessions.drop_table()
        exhibitions.drop_table()

    if conn:
        conn.close()
