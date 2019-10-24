set PGPASSWORD=postgres
psql  -U postgres -w -f "C:\Distr\sqlss.sql"
echo \q
pg_restore -U postgres -w -d "preferentum_db" C:\Distr\Preferentum\db\1.bak
pause