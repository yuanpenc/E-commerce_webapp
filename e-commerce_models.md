## Account System

| username | password | email | is_active | third_party |
| -------- | -------- | ----- | --------- | ----------- |
| /        | /        | /     | /         | /           |

## User System
| nickname | follow_stores | likes    | is_active | user    |
| -------- | -------- | -------- | --------- | -------------- |
| /     | /     | / | /  | foreign key |

## Delivery System

| recipient_name | recipient_addr | zip_code | recipient_phone | is_default                         | passport    | from           |
| -------------- | -------------- | -------- | --------------- | ---------------------------------- | ----------- | -------------- |
| name           | address        | zip      | phone number    | is default delivery address or not | foreign key | source address |

## Product System

| name         | desc                | price      | unit | stock | sales | detail | image | status         | type_id            | is_deal        |
| ------------ | ------------------- | ---------- | ---- | ----- | ----- | ------ | ----- | -------------- | ------------------ | -------------- |
| product name | Product description | item price | unit | stock | sales | detail | image | On sale status | product categories | Is deal or not |

## Order System

### Order Info System

| order_id                           | passport    | addr        | total_count  | total_price | transit_price | pay_method | trade_id |      |
| ---------------------------------- | ----------- | ----------- | ------------ | ----------- | ------------- | ---------- | -------- | ---- |
| timestamp+passport_id，primary key | Foreign Key | Foreign Key | total number | Total prize | Transit fee   | Pay method | trade id |      |

### Order Product System

| order       | items       | count   | price |      |
| ----------- | ----------- | ------- | ----- | ---- |
| Foreign Key | Foreign Key | Account | Prize |      |

