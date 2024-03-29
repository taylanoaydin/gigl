DROP TABLE IF EXISTS apps;
DROP TABLE IF EXISTS gigs;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS bookmarks;
DROP TABLE IF EXISTS banned_users;

CREATE TABLE users
(
  netid VARCHAR(10) PRIMARY KEY,
  name TEXT,
  visible BOOLEAN NOT NULL,
  bio VARCHAR(1000),
  links TEXT,
  specialty TEXT,
  last_active DATE
);
create INDEX index_users_visible ON users(visible);
create INDEX index_users_specialty ON users(specialty);
create INDEX index_users_active ON users(last_active);

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

ALTER TABLE gigs
ADD COLUMN num_apps integer DEFAULT 0;

ALTER TABLE users
ADD COLUMN banned boolean not null DEFAULT FALSE;

CREATE INDEX index_users_banned ON users(banned);

CREATE INDEX index_gigs_apps ON gigs(num_apps);

CREATE TABLE apps
(
  netid VARCHAR(10),
  gigID INTEGER,
  message VARCHAR(1000),
  PRIMARY KEY (netid, gigID)
);

CREATE TYPE status_type AS ENUM ('YES', 'UNDECIDED', 'NO');

ALTER TABLE apps
ADD COLUMN status status_type DEFAULT 'UNDECIDED';

CREATE TABLE bookmarks
(
  netid VARCHAR(10),
  gigID INTEGER,
  PRIMARY KEY (netid, gigID)
);

ALTER TABLE gigs
ADD COLUMN price DECIMAL(5,2);