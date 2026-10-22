# ERD (Crow's Foot)

## Сущности

### User

| Поле       | Тип      | Ограничение       |
| ---------- | -------- | ----------------- |
| user_id    | INTEGER  | PK, autoincrement |
| name       | VARCHAR  | NOT NULL          |
| phone      | VARCHAR  | UNIQUE, NOT NULL  |
| email      | VARCHAR  | UNIQUE            |
| rating     | FLOAT    | DEFAULT 5.0       |
| created_at | DATETIME | DEFAULT now()     |

### Trip

| Поле           | Тип      | Ограничение         |
| -------------- | -------- | ------------------- |
| trip_id        | INTEGER  | PK                  |
| driver_id      | INTEGER  | FK → User.user_id   |
| origin         | VARCHAR  | NOT NULL            |
| destination    | VARCHAR  | NOT NULL            |
| departure_time | DATETIME | NOT NULL            |
| seats_total    | INTEGER  | NOT NULL, CHECK > 0 |
| price_per_seat | FLOAT    | NOT NULL, CHECK > 0 |
| status         | VARCHAR  | DEFAULT 'ACTIVE'    |

### Booking

| Поле         | Тип      | Ограничение       |
| ------------ | -------- | ----------------- |
| booking_id   | INTEGER  | PK                |
| trip_id      | INTEGER  | FK → Trip.trip_id |
| passenger_id | INTEGER  | FK → User.user_id |
| status       | VARCHAR  | DEFAULT 'PENDING' |
| created_at   | DATETIME | DEFAULT now()     |

### Review

| Поле       | Тип     | Ограничение             |
| ---------- | ------- | ----------------------- |
| review_id  | INTEGER | PK                      |
| booking_id | INTEGER | FK → Booking.booking_id |
| author_id  | INTEGER | FK → User.user_id       |
| target_id  | INTEGER | FK → User.user_id       |
| score      | INTEGER | CHECK 1..5              |
| comment    | TEXT    |                         |

## Связи
