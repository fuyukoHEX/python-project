-- TSIS1 - New procedures and functions (PL/pgSQL)
-- Run after schema.sql

-- Add phone to existing contact. Ex: CALL add_phone('Amir', '+77001234567', 'mobile');
CREATE OR REPLACE PROCEDURE add_phone(p_cname VARCHAR, p_phone VARCHAR, p_type VARCHAR) LANGUAGE plpgsql AS $$
DECLARE v_cid INTEGER;
BEGIN
    SELECT id INTO v_cid FROM contacts WHERE name = p_cname;
    IF v_cid IS NULL THEN RAISE EXCEPTION 'Contact "%" not found', p_cname; END IF;
    INSERT INTO phones (contact_id, phone, type) VALUES (v_cid, p_phone, p_type);
END; $$;

-- Move contact to group (creates if missing). Ex: CALL move_to_group('Amir', 'VIP');
CREATE OR REPLACE PROCEDURE move_to_group(p_cname VARCHAR, p_gname VARCHAR) LANGUAGE plpgsql AS $$
DECLARE v_cid INTEGER; v_gid INTEGER;
BEGIN
    SELECT id INTO v_cid FROM contacts WHERE name = p_cname;
    IF v_cid IS NULL THEN RAISE EXCEPTION 'Contact "%" not found', p_cname; END IF;
    SELECT id INTO v_gid FROM groups WHERE name = p_gname;
    IF v_gid IS NULL THEN INSERT INTO groups (name) VALUES (p_gname) RETURNING id INTO v_gid; END IF;
    UPDATE contacts SET group_id = v_gid WHERE id = v_cid;
END; $$;

-- Search by name, email, or phone. Ex: SELECT * FROM search_contacts('gmail');
CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT) RETURNS TABLE(contact_id INTEGER, name VARCHAR, email VARCHAR, phone VARCHAR, phone_type VARCHAR) AS $$
BEGIN
    RETURN QUERY SELECT DISTINCT c.id, c.name, c.email, p.phone, p.type FROM contacts c
    LEFT JOIN phones p ON p.contact_id = c.id
    WHERE c.name ILIKE '%'||p_query||'%' OR c.email ILIKE '%'||p_query||'%' OR p.phone ILIKE '%'||p_query||'%' ORDER BY c.name;
END; $$ LANGUAGE plpgsql;

-- Paginated contacts. Ex: SELECT * FROM get_contacts_paginated(5, 0);
CREATE OR REPLACE FUNCTION get_contacts_paginated(p_limit INT, p_offset INT) RETURNS TABLE(id INTEGER, name VARCHAR, email VARCHAR, birthday DATE, grp VARCHAR) AS $$
BEGIN
    RETURN QUERY SELECT c.id, c.name, c.email, c.birthday, g.name AS grp FROM contacts c
    LEFT JOIN groups g ON g.id = c.group_id ORDER BY c.name LIMIT p_limit OFFSET p_offset;
END; $$ LANGUAGE plpgsql;
