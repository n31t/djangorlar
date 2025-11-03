// Use DBML to define your database structure
// Docs: https://dbml.dbdiagram.io/docs

Table restaurants {
  id integer [pk, increment]
  name varchar(255) [not null]
  description text
  cuisine_id int [not null]
  rating int [default: 0]
  geojson text [not null] // some geo data maybe coordinates or smth like that
}

Table dishes {
  id integer [pk, increment]
  category_id int [not null]
  restaurant_id int [not null]
  name varchar(255) [not null]
  description text
  price int [not null]
}

Table categories {
  id integer [pk, increment]
  parent_category int
  name varchar(255) [not null]
}

Table cuisines {
  id integer [pk, increment]
  name varchar(255) [not null]
  description text
}

Table options {
  id integer [pk, increment]
  dish_id int [not null]
  name varchar(255) [not null]
  price int [not null]
}

Table delivery_zone {
  id integer [pk, increment]
  restaurant_id int [not null]
  geojson text [not null] // some geo data maybe coordinates or smth like that
  min_delivery_price int [not null]
}


// Relationships
Ref: restaurants.cuisine_id > cuisines.id
Ref: dishes.category_id > categories.id
Ref: dishes.restaurant_id > restaurants.id
Ref: options.dish_id > dishes.id
Ref: delivery_zone.restaurant_id > restaurants.id
Ref: categories.parent_category > categories.id



Enum order_status {
  new
  confirmed
  delivering
  done
}

Enum payment_status {
  pending
  authorized
  failed
  refunded
}

Table users {
  id int [pk, increment]
  email varchar(255) [not null, unique]
  full_name varchar(255)
  is_active boolean [not null, default: true]
  created_at timestamp [default: `now()`]
  updated_at timestamp [default: `now()`]
}

Table addresses {
  id int [pk, increment]
  user_id int [not null]
  street varchar(255) [not null]
  city varchar(100) [not null]
  country char(2)
  created_at timestamp [default: `now()`]
  updated_at timestamp [default: `now()`]
}

Table orders {
  id int [pk, increment]
  user_id int [not null]
  restaurant_id int [not null]
  address_id int [not null]
  status order_status [not null, default: 'new']
  subtotal int [not null]
  discount_total int [not null, default: 0]
  total int [not null]
  placed_at timestamp [not null, default: `now()`]
  created_at timestamp [default: `now()`]
  updated_at timestamp [default: `now()`]
}

Table order_items {
  id int [pk, increment]
  order_id int [not null]
  dish_id int
  quantity int [not null, default: 1]
  total int [not null]
  created_at timestamp [default: `now()`]
  updated_at timestamp [default: `now()`]
}

Table order_item_options {
  id int [pk, increment]
  order_item_id int [not null]
  option_id int
  option_name varchar(255) [not null]
  price_delta int [not null, default: 0]
  created_at timestamp [default: `now()`]
  updated_at timestamp [default: `now()`]
}

Table promo_codes {
  id int [pk, increment]
  code varchar(64) [not null, unique]
  description text
  discount float
  is_active boolean [not null, default: true]
  valid_from timestamp
  valid_to timestamp
  created_at timestamp [default: `now()`]
  updated_at timestamp [default: `now()`]
}

Table order_promos {
  id int [pk, increment]
  order_id int [not null]
  promo_code_id int [not null]
  created_at timestamp [default: `now()`]
  updated_at timestamp [default: `now()`]
}

Table payments {
  id int [pk, increment]
  order_id int [not null]
  amount int [not null]
  method varchar(50) [not null]
  status payment_status [not null, default: 'pending']
  created_at timestamp [not null, default: `now()`]
}


// Relationships
Ref: orders.restaurant_id > restaurants.id
Ref: order_items.dish_id > dishes.id
Ref: order_item_options.option_id > options.id

Ref: addresses.user_id > users.id
Ref: orders.user_id > users.id
Ref: orders.address_id > addresses.id

Ref: order_items.order_id > orders.id
Ref: order_item_options.order_item_id > order_items.id

Ref: order_promos.order_id > orders.id
Ref: order_promos.promo_code_id > promo_codes.id

Ref: payments.order_id > orders.id
