create table
  public.items (
    id bigint generated by default as identity,
    name text null,
    constraint items_pkey primary key (id)
  ) tablespace pg_default;
INSERT INTO public.items
(name)
VALUES
('Ketchup');
  
create table
  public.stores (
    id bigint generated by default as identity,
    name text null,
    constraint stores_pkey primary key (id)
  ) tablespace pg_default;
INSERT INTO public.stores
(name)
VALUES
('Safeway');
  
create table
  public.users (
    id bigint generated by default as identity,
    name text null,
    email text null,
    constraint users_pkey primary key (id)
  ) tablespace pg_default;
INSERT INTO public.users
(name,email)
VALUES
('Kevin Johnson','kj@gmail.com');
create table
  public.crowdsourced_entries (
    id bigint generated by default as identity,
    created_at timestamp with time zone not null default now(),
    item_id bigint null,
    user_id bigint null,
    price numeric null,
    inventory text null,
    store_id bigint null,
    constraint corwdsourced_entries_pkey primary key (id),
    constraint crowdsourced_entries_item_id_fkey foreign key (item_id) references items (id),
    constraint crowdsourced_entries_store_id_fkey foreign key (store_id) references stores (id),
    constraint crowdsourced_entries_user_id_fkey foreign key (user_id) references users (id)
  ) tablespace pg_default;

create table
  public.grocery_list (
    id bigint generated by default as identity,
    user_id bigint null,
    constraint grocery_list_pkey primary key (id),
    constraint grocery_list_user_id_fkey foreign key (user_id) references users (id)
  ) tablespace pg_default;

create table
  public.grocery_list_items (
    id bigint generated by default as identity,
    list_id bigint null,
    item_id bigint null,
    constraint grocery_list_items_pkey primary key (id),
    constraint grocery_list_items_item_id_fkey foreign key (item_id) references items (id),
    constraint grocery_list_items_list_id_fkey foreign key (list_id) references grocery_list (id)
  ) tablespace pg_default;