# **Environment setup**
#### 1. Create a Google Service Account
Follow this link to create a service account:
https://console.cloud.google.com/iam-admin/serviceaccounts

#### 2. Create a JSON key
Go to: 
IAM & Admin → Service Accounts → Your Account → Keys \
Then click "Add Key" → "Create new key", and select the JSON format. \
![img.png](readme_sources/img.png)

#### 3. Add the JSON key to your project

#### 4. Create .env file:
Provide following variables: \
`GOOGLE_APPLICATION_CREDENTIALS` - path to your json file \
`GCP_LOCATION` - us-central1(default) \
`GCP_PROJECT` - "project_id" from json file

#### 5. Run Docker-compose
#### 6. Send Debezium json config from bootstrap..