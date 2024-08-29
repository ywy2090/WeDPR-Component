
CREATE TABLE t_job_worker (
    worker_id VARCHAR(100) PRIMARY KEY,
    job_id VARCHAR(255) INDEX,
    type VARCHAR(255),
    status VARCHAR(255),
    upstreams TEXT,
    inputs_statement TEXT,
    outputs TEXT,
    create_time BIGINT,
    update_time BIGINT
)ENGINE=InnoDB default charset=utf8mb4 default collate=utf8mb4_unicode_ci;

CREATE TABLE t_computing_node (
    id VARCHAR(255) PRIMARY KEY,
    url VARCHAR(255),
    type VARCHAR(255),
    loading INT
)ENGINE=InnoDB default charset=utf8mb4 default collate=utf8mb4_unicode_ci;


INSERT INTO t_computing_node (id, url, type, loading)
VALUES
    ("001", '127.0.0.1:10200', 'PSI', 0),
    ("002", '127.0.0.1:10201', 'MPC', 0),
    ("003", '127.0.0.1:10202', 'MODEL', 0);
