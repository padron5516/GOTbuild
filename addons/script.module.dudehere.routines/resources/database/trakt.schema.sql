CREATE TABLE IF NOT EXISTS "version" (
	"db_version" INTEGER DEFAULT 1 UNIQUE,
	PRIMARY KEY(db_version)
);

CREATE TABLE IF NOT EXISTS "activities" (
	"id" INTEGER PRIMARY KEY AUTOINCREMENT,
	"activity" TEXT UNIQUE,
	"ts" TIMESTAMP
);

DELETE FROM "activities" WHERE 1;

DROP TABLE "tvshows";

DROP TABLE "movies";

DROP TABLE "episodes";

DELETE FROM "activity_cache" WHERE 1;

CREATE TABLE IF NOT EXISTS "activity_cache" (
	"id" INTEGER PRIMARY KEY AUTOINCREMENT,
	"activity" TEXT UNIQUE,
	"cache" TEXT
);

CREATE TABLE IF NOT EXISTS "cache" (
	"id" INTEGER PRIMARY KEY AUTOINCREMENT,
	"hash_id" TEXT UNIQUE,
	"media" TEXT,
	"url" TEXT,
	"results" TEXT,
	"ts" TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
);

CREATE TABLE IF NOT EXISTS "id_cache" (
	"id" INTEGER PRIMARY KEY AUTOINCREMENT,
	"title" TEXT,
	"year" INTEGER,
	"media" TEXT,
	"imdb_id" TEXT UNIQUE,
	"tmdb_id" TEXT,
	"trakt_id" INTEGER
);

CREATE TABLE IF NOT EXISTS "show_cache"(
	"id" INTEGER PRIMARY KEY AUTOINCREMENT,
	"title" TEXT,
	"imdb_id" TEXT,
	"tmdb_id" TEXT,
	"tvdb_id" TEXT,
	"trakt_id" TEXT,
	"slug" TEXT,
	"cache" TEXT,
	UNIQUE (imdb_id, tmdb_id, title)
);

CREATE TABLE IF NOT EXISTS "episode_cache"(
	"id" INTEGER PRIMARY KEY AUTOINCREMENT,
	"imdb_id" TEXT,
	"tmdb_id" TEXT,
	"tvdb_id" TEXT,
	"trakt_id" TEXT,
	"slug" TEXT,
	"season" INTEGER,
	"episode" INTEGER,
	"cache" TEXT,
	UNIQUE (imdb_id, tmdb_id, season, episode)
);

CREATE TABLE IF NOT EXISTS "movie_cache"(
	"id" INTEGER PRIMARY KEY AUTOINCREMENT,
	"title" TEXT,
	"imdb_id" TEXT,
	"tmdb_id" TEXT,
	"tvdb_id" TEXT,
	"trakt_id" TEXT,
	"slug" TEXT,
	"cache" TEXT,
	UNIQUE (imdb_id, tmdb_id, title)
);

CREATE TABLE IF NOT EXISTS "sync_states"(
	"id" INTEGER PRIMARY KEY AUTOINCREMENT,
	"name" TEXT,
	"slug" TEXT UNIQUE,
	"sync" INTEGER DEFAULT 1
);

CREATE VIEW IF NOT EXISTS "stale_cache" AS
	SELECT id, 
	hash_id, 
	strftime("%s",'now') -  strftime("%s",ts) > (3600 * 2) AS stale 
	FROM cache 
	WHERE stale = 1
;
