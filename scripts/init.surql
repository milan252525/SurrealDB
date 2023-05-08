DEFINE NS NDBI040;
USE NS NDBI040;

DEFINE DB reviews;
USE DB reviews;

DEFINE TABLE user SCHEMAFULL;
DEFINE FIELD name ON TABLE user TYPE string;
DEFINE FIELD surname ON TABLE user TYPE string;
DEFINE FIELD email ON TABLE user TYPE string ASSERT $value != NONE AND is::email($value);
DEFINE INDEX user_email_unique ON TABLE user COLUMNS email UNIQUE;

DEFINE TABLE restaurant;
DEFINE FIELD name ON TABLE restaurant TYPE string;
DEFINE FIELD location ON TABLE restaurant TYPE geometry (point);

DEFINE TABLE city; 
DEFINE FIELD name ON TABLE city TYPE string;
DEFINE FIELD center ON TABLE city TYPE geometry (point);

DEFINE TABLE food;
DEFINE FIELD name ON TABLE food TYPE string;
DEFINE FIELD ingredients ON TABLE food TYPE array;
