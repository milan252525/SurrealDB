# Starting database in a memory as a root user
surreal start --log debug --user root --pass root memory

# Connecting to the database through CLI
surreal sql --conn http://localhost:8000 --user root --pass root --ns NDBI040 --db reviews 