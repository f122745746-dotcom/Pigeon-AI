-- Pigeon-AI database schema
-- Target database: PostgreSQL 13+
-- Enable gen_random_uuid() for UUID primary keys.
CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email TEXT UNIQUE,
    phone TEXT,
    name TEXT,
    role TEXT NOT NULL DEFAULT 'user',
    membership_level TEXT NOT NULL DEFAULT 'free',
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT users_email_or_phone CHECK (email IS NOT NULL OR phone IS NOT NULL)
);

CREATE TABLE IF NOT EXISTS pigeon (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    owner_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    ring_number TEXT NOT NULL UNIQUE,
    name TEXT,
    gender TEXT CHECK (gender IN ('male', 'female', 'unknown')),
    color TEXT,
    birth_date DATE,
    status TEXT NOT NULL DEFAULT 'active',
    father_ring TEXT,
    mother_ring TEXT,
    photo_url TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS pedigree (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    pigeon_id UUID NOT NULL REFERENCES pigeon(id) ON DELETE CASCADE,
    generation INTEGER NOT NULL CHECK (generation >= 1),
    father_id UUID REFERENCES pigeon(id) ON DELETE SET NULL,
    mother_id UUID REFERENCES pigeon(id) ON DELETE SET NULL,
    CONSTRAINT pedigree_unique_generation UNIQUE (pigeon_id, generation),
    CONSTRAINT pedigree_not_self_father CHECK (father_id IS NULL OR father_id <> pigeon_id),
    CONSTRAINT pedigree_not_self_mother CHECK (mother_id IS NULL OR mother_id <> pigeon_id)
);

CREATE TABLE IF NOT EXISTS breeding_record (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    male_pigeon_id UUID NOT NULL REFERENCES pigeon(id) ON DELETE CASCADE,
    female_pigeon_id UUID NOT NULL REFERENCES pigeon(id) ON DELETE CASCADE,
    breed_date DATE NOT NULL,
    success_date DATE,
    egg_count INTEGER CHECK (egg_count IS NULL OR egg_count >= 0),
    hatch_count INTEGER CHECK (hatch_count IS NULL OR hatch_count >= 0),
    ring_date DATE,
    notes TEXT,
    CONSTRAINT breeding_pair_not_same CHECK (male_pigeon_id <> female_pigeon_id)
);

CREATE TABLE IF NOT EXISTS health_record (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    pigeon_id UUID NOT NULL REFERENCES pigeon(id) ON DELETE CASCADE,
    record_type TEXT NOT NULL,
    symptom TEXT,
    medicine TEXT,
    result TEXT,
    status TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS race_record (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    pigeon_id UUID NOT NULL REFERENCES pigeon(id) ON DELETE CASCADE,
    club_name TEXT,
    season TEXT,
    race_name TEXT NOT NULL,
    race_date DATE NOT NULL,
    weather TEXT,
    rank INTEGER CHECK (rank IS NULL OR rank >= 1),
    speed NUMERIC(10, 3) CHECK (speed IS NULL OR speed >= 0),
    score NUMERIC(10, 2),
    prize_money NUMERIC(12, 2) CHECK (prize_money IS NULL OR prize_money >= 0)
);

CREATE TABLE IF NOT EXISTS ai_analysis (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    pigeon_id UUID NOT NULL REFERENCES pigeon(id) ON DELETE CASCADE,
    analysis_type TEXT NOT NULL,
    analysis_json JSONB NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS files (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    owner_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    file_type TEXT NOT NULL,
    file_url TEXT NOT NULL,
    file_name TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS notifications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    message TEXT NOT NULL,
    is_read BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS weather_cache (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    city TEXT NOT NULL UNIQUE,
    temperature NUMERIC(5, 2),
    wind_speed NUMERIC(6, 2),
    wind_direction TEXT,
    humidity NUMERIC(5, 2) CHECK (humidity IS NULL OR (humidity >= 0 AND humidity <= 100)),
    forecast_json JSONB,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_pigeon_owner_id ON pigeon(owner_id);
CREATE INDEX IF NOT EXISTS idx_pigeon_ring_number ON pigeon(ring_number);
CREATE INDEX IF NOT EXISTS idx_pedigree_pigeon_id ON pedigree(pigeon_id);
CREATE INDEX IF NOT EXISTS idx_pedigree_father_id ON pedigree(father_id);
CREATE INDEX IF NOT EXISTS idx_pedigree_mother_id ON pedigree(mother_id);
CREATE INDEX IF NOT EXISTS idx_breeding_record_male_id ON breeding_record(male_pigeon_id);
CREATE INDEX IF NOT EXISTS idx_breeding_record_female_id ON breeding_record(female_pigeon_id);
CREATE INDEX IF NOT EXISTS idx_health_record_pigeon_id ON health_record(pigeon_id);
CREATE INDEX IF NOT EXISTS idx_race_record_pigeon_id ON race_record(pigeon_id);
CREATE INDEX IF NOT EXISTS idx_race_record_race_date ON race_record(race_date);
CREATE INDEX IF NOT EXISTS idx_ai_analysis_pigeon_id ON ai_analysis(pigeon_id);
CREATE INDEX IF NOT EXISTS idx_files_owner_id ON files(owner_id);
CREATE INDEX IF NOT EXISTS idx_notifications_user_id ON notifications(user_id);
CREATE INDEX IF NOT EXISTS idx_notifications_unread ON notifications(user_id, is_read) WHERE is_read = false;
CREATE INDEX IF NOT EXISTS idx_weather_cache_city ON weather_cache(city);

CREATE OR REPLACE FUNCTION set_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_users_updated_at
BEFORE UPDATE ON users
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();
