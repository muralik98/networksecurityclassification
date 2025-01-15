import dagshub

# Add the token to the DagsHub authentication cache
token = "4621a495f1943c8dc02291e5757947866bd85b9d"
dagshub.auth.add_app_token(token)

# Initialize the repository with the token cached
dagshub.init(repo_owner='muralik98', repo_name='networksecurityclassification', mlflow=True)