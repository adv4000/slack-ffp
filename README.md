# Find who was Fired and no longer in Slack

### You just need to Generate User Token using Slack App!

1. Goto: `https://api.slack.com/apps` and login to your Slack Workspace
2. Click: Create an App
3. Select: From scratch
4. App Name: Demo
5. Select Workspace from Step-1
6. Click: Create App
7. Goto: OAuth & Permissions
8. Goto: Scopes -> User Token Scopes
9. Click: Add an Oauth Scope
10. Select `users:read`
11. Scroll up and Click Install to <Your_Workspace>
12. Once Approved by Workspace Admin, you will get your TOKEN `xoxp-`
13. In Python Script set your TOKEN

### You can test TOKEN with CURL command:
```
curl -X GET "https://slack.com/api/users.list" -H "Authorization: Bearer xoxp-2704744787926-your-user-token-7086d8c9477484166"
```

Copyleft(c) by Denis Astahov.