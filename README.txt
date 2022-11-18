This telegram bot using for viewing user offers.
DataBase : Postgres
Admin functions:

    /get_offers, /next => Bot give you a user offer.
        /next -> Give you an offer.
        /contact -> Give you a link(work only on phones) on user.
        /block -> Plus chance, if user have limit of chance , bot blocked this person.
        /unblock -> Minus chance, if user was blocked unblock him.
        quit -> you end /get_offers.

    /get_seen_offers => Bot send you "Start successfully" . # limit 100 seen offers.
        /skip_seen -> Give you a seen offer.
        /contact -> Give you a link(work only on phones) on user.
        /block -> Plus chance, if user have limit of chance , bot blocked this person.
        /unblock -> Minus chance, if user was blocked unblock him.
        quit -> you end /get_offers.

    /clean_DB => Bot del all seen messages in table.
        confirming -> you will write "yes" or "no".
        if you write "yes":
            password -> you will write pin that bot sends you if you write pin with mistake /clean_DB function is over.
            After password confirming bot del all seen messages in message table. # "message" table is default name.
        if you write "no":
            /clean_DB function is over.

User functions:

    /create_offer => User can create offer which upload in database.
        confirming -> User have two ways confirm and rewrite.
        if user push "rewrite" button:
            User will send message and confirm message.
    /my_offers => Bot send user offer(s) for all time.
        /del_offers -> User can delete all his offers.
        /quit -> end function /my_offers.

    /help => Bot send message that you want.
        You can set this message in global_variables/class BotSet/HELP_AND_START_TEXT

::::::::::::::::::::::::::::::::::CUSTOM DATABASE::::::::::::::::::::::::::::::::::
If you want connect to the bot your own database this section for you.
I wrote my bot with Postgres database so if you want to connect other database
you will rewrite all SQL requests in :
    class DataBaseInterface (path: magic_with_database/work_with_DB.py)
    class TableCreator (path: magic_with_database/create_table.py) -> if you want to create table in one click
                                                                      rewrite this class too.

If you want to create your tables you can use my request how base SQL request
Create User table:
    CREATE TABLE  user_table(
    id SERIAL PRIMARY KEY,
    user_chat_id bigint NOT NULL,
    chance_limit integer NOT NULL,
    user_first_name VARCHAR);
    # example request
    # language Postgres --latest

Create Message table:
    CREATE TABLE  message_table(
    id SERIAL PRIMARY KEY,
    user_chat_id bigint NOT NULL,
    message VARCHAR NOT NULL,
    seen boolean NOT NULL);
    # example request
    # language Postgres --latest

Bot created by De_Santos (Misha)
Thanks :3