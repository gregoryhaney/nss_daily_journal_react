CREATE TABLE entries (
    id INTEGER PRIMARY KEY,
    date VARCHAR(10),
    entry VARCHAR(200),
    concept VARCHAR(30),
    moodId INTEGER(2),
    FOREIGN KEY (moodId) REFERENCES moods(id)
    );


CREATE TABLE moods (
    id INTEGER PRIMARY KEY,
    label VARCHAR(15)
    );

INSERT INTO entries VALUES (NULL,"20220411","I do not miss JavaScript. It was sorta fun, but I'm over it.","JavaScript",2);
INSERT INTO entries VALUES (NULL,"20220412","Looking for help with imposter syndrome.","Developing",5);
INSERT INTO entries VALUES (NULL,"20220410","SQL is not my friend.","SQL",8);
INSERT INTO entries VALUES (NULL,"20220409","Cannot wait unitl we learn Django.","Django",9);
INSERT INTO entries VALUES (NULL,"20220409","I thought SQL was supposed to be difficult. Mmmffph!","SQL",6);


INSERT INTO moods VALUES (NULL, "Happy");
INSERT INTO moods VALUES (NULL, "Glad");
INSERT INTO moods VALUES (NULL, "Lonely");
INSERT INTO moods VALUES (NULL, "Overwhelmed");
INSERT INTO moods VALUES (NULL, "Underwhelmed");
INSERT INTO moods VALUES (NULL, "Nervous");
INSERT INTO moods VALUES (NULL, "Scared");
INSERT INTO moods VALUES (NULL, "Bold");


SELECT *
        FROM entries AS e
        WHERE e.entry LIKE "%learn%"
            OR e.concept LIKE "%learn%";
          

UPDATE entries
        SET entry = "More fun with flags"
        WHERE id = 5;

UPDATE entries
    SET id = 13
    WHERE entry LIKE "TEST7";

DROP table entries;
DROP table moods;