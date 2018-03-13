# Navigate to scripts folder
cd src/public/js &&

# Clean up
touch constants.js && rm -rf constants.js &&

# Create Constants.js based on environment type
if [[ "$NODE_ENV" == "production" ]]; then
    echo "var APIURL = \"https://adpq.hotbsoftware.com/api/v1/\";\nvar SocialMediaURL = \"https://adpq.hotbsoftware.com/\";" > 'constants.js';
elif [[ "$NODE_ENV" == "staging" ]]; then
    echo "var APIURL = \"https://adpq-staging.hotbsoftware.com/api/v1/\";\nvar SocialMediaURL = \"https://adpq-staging.hotbsoftware.com/\";" > 'constants.js';
elif [[ "$NODE_ENV" == "local" ]]; then
    echo "var APIURL = \"http://localhost:3001/api/v1/\";\nvar SocialMediaURL = \"http://localhost:3001/\";" > 'constants.js';
else # defaults to staging if undefined
    echo "var APIURL = \"https://adpq-staging.hotbsoftware.com/api/v1/\";\nvar SocialMediaURL = \"https://adpq-staging.hotbsoftware.com/\";" > 'constants.js';
fi