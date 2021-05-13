BEGIN;

CREATE TABLE "date" (
    day_id INTEGER NOT NULL PRIMARY KEY,
    day TEXT NOT NULL,
    sorder INTEGER NOT NULL,
    UNIQUE(sorder ASC) 
    UNIQUE(day_id ASC) 
    UNIQUE(day ASC)
);

INSERT INTO date(day_id, day, sorder) VALUES(0, 'Sunday', 7);
INSERT INTO date(day_id, day, sorder) VALUES(1, 'Monday', 1);
INSERT INTO date(day_id, day, sorder) VALUES(2, 'Tuesday', 2);
INSERT INTO date(day_id, day, sorder) VALUES(3, 'Wednesday', 3);
INSERT INTO date(day_id, day, sorder) VALUES(4, 'Thursday', 4);
INSERT INTO date(day_id, day, sorder) VALUES(5, 'Friday', 5);
INSERT INTO date(day_id, day, sorder) VALUES(6, 'Saturday', 6);

COMMIT;