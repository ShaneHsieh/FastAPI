-- 創建使用者（如果還不存在）
DO $$ 
BEGIN
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'fastapi_user') THEN
        CREATE USER fastapi_user WITH PASSWORD 'password';
    END IF;
END $$;

DO $$ 
BEGIN
   IF NOT EXISTS (SELECT FROM pg_database WHERE datname = 'fastapi_db') THEN
      CREATE DATABASE fastapi_db OWNER fastapi_user;
   END IF;
END $$;

-- 授權使用者對資料庫的所有權限
GRANT ALL PRIVILEGES ON DATABASE fastapi_db TO fastapi_user;

CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price FLOAT NOT NULL,
    description TEXT,
    stock INTEGER NOT NULL DEFAULT 0,
    category VARCHAR(255),
    discount FLOAT NOT NULL DEFAULT 0.0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS suppliers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    contact_info TEXT,
    rating FLOAT DEFAULT 0.0
);

CREATE TABLE IF NOT EXISTS product_supplier (
    product_id INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    supplier_id INTEGER NOT NULL REFERENCES suppliers(id) ON DELETE CASCADE,
    PRIMARY KEY (product_id, supplier_id)
);

CREATE TABLE IF NOT EXISTS product_histories (
    id SERIAL PRIMARY KEY,
    product_id INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    price FLOAT NOT NULL,
    stock INTEGER NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);