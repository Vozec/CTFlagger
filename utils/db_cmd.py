CMD_create_table = """
CREATE TABLE IF NOT EXISTS files (
	hash TEXT PRIMARY KEY UNIQUE,
	filename TEXT NOT NULL,
	ext TEXT NOT NULL,
	status TEXT NOT NULL ,
	path_up TEXT NOT NULL,
	first_up INT NOT NULL,
	last_up INT NOT NULL,
	size INT NOT NULL,
	upload_count INT NOT NULL,
	magic TEXT NOT NULL,
	all_password BLOB,
	flag BLOB,
	result TEXT,
	progress TEXT
) WITHOUT ROWID;
"""[1:-1]

CMD_add_file = "INSERT INTO files VALUES(:hash,:filename,:ext,:status,:path_up,:first_up,:last_up,:size,:upload_count,:magic,:all_password,:flag,:result,:progress)"

CMD_get_by_hash = "SELECT * FROM files WHERE hash = :hash"

CMD_get_status_by_hash = "SELECT status FROM files WHERE hash = :hash"

CMD_get_progress_by_hash = "SELECT progress FROM files WHERE hash = :hash"

CMD_update_info = "UPDATE files SET last_up = :last_up , upload_count = :upload_count , all_password = :all_password  WHERE hash = :hash"

CMD_update_status = "UPDATE files SET status = :status WHERE hash = :hash"

CMD_update_result = "UPDATE files SET result = :result WHERE hash = :hash"

CMD_update_progress = "UPDATE files SET progress = :progress WHERE hash = :hash"

CMD_update_flag = "UPDATE files SET flag = :flag WHERE hash = :hash"