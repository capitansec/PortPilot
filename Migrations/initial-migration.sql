CREATE TABLE IF NOT EXISTS public.users (
    id serial PRIMARY KEY,
    uuid uuid NOT NULL,
    username character varying NOT NULL,
    email character varying NOT NULL,
    password character varying(64) NOT NULL,
    created timestamp with time zone DEFAULT current_timestamp
);


ALTER TABLE IF EXISTS public.users
    ADD CONSTRAINT users_uuid_key UNIQUE (uuid);

CREATE INDEX IF NOT EXISTS ix_users_email ON public.users USING btree (email);
CREATE INDEX IF NOT EXISTS ix_users_id ON public.users USING btree (id);
CREATE UNIQUE INDEX IF NOT EXISTS ix_users_username ON public.users USING btree (username);
