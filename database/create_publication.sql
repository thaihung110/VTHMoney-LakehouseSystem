-- Enable logical replication for the database
ALTER SYSTEM SET wal_level = logical;

-- Create the publication for all tables
CREATE PUBLICATION dbz_publication FOR ALL TABLES;

-- Grant necessary permissions
ALTER PUBLICATION dbz_publication OWNER TO admin; 