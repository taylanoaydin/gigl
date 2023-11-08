DROP TABLE IF EXISTS apps;
DROP TABLE IF EXISTS gigs;
DROP TABLE IF EXISTS users;

CREATE TABLE users
(
  netid VARCHAR(10) PRIMARY KEY,
  name TEXT,
  visible BOOLEAN NOT NULL,
  bio VARCHAR(1000),
  links TEXT
);

CREATE TABLE gigs
(
  gigID SERIAL PRIMARY KEY,
  netid VARCHAR(10),
  title VARCHAR(100),
  category TEXT,
  description VARCHAR(1000),
  qualf VARCHAR(500),
  startfrom DATE,
  until DATE,
  posted DATE
);
CREATE INDEX index_gigs_netid ON gigs(netid);
CREATE INDEX index_gigs_posted ON gigs(posted);
CREATE INDEX index_gigs_category ON gigs(category);


CREATE TABLE apps
(
  netid VARCHAR(10),
  gigID INTEGER,
  message VARCHAR(1000),
  PRIMARY KEY (netid, gigID)
);
