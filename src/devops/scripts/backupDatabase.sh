#
#  backupDatabase.sh
#  created by HOTB Software 
#

# Constants (Please make sure to enter all constants)
dbUrl=
port=
dbName=
username=
password=

# Validate that all constants are correctly defined
if [ -z "$dbUrl" ] || [ -z "$port" ] || [ -z "$dbName" ] || [ -z "$username" ] || [ -z "$password" ]; then
  echo 'WARNING: One or more variables are undefined. Please edit the following file: backupProductionDatabase.sh'        
  exit 1
fi

# Export all data from Mongo DB
mongodump --host $dbUrl --port $port -u $username -p $password --authenticationDatabase admin -d $dbName --out ./database/backups/ &&

# Get current date & time
dateTime=$(date +%Y-%m-%d-%H:%M:%S)

# Send all collections to AWS S3
for file in ./database/backups/ADPQ/*; do
    filename=$(basename $file)
    aws s3 cp $file s3://adpq-assets/databaseBackups/$dateTime/$filename
done

# Cleanup
rm -rf ./database/backups/*