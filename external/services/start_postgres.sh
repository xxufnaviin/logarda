source ./services/.envrc

# starts posgres container in background on port 5432 with the name "logarda-metrics" username is default = postgres
docker run --name logarda-metrics -e POSTGRES_PASSWORD=POSTGRES_PASSWORD -p 5432:5432 -v ~/metrics:/var/lib/postgresql -d postgres