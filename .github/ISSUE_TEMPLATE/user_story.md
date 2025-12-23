---
**As a** customer
**I need** to retrieve an account by its ID from the account service
**So that** I can view my account details

### Details and Assumptions
* The service exposes a REST API endpoint to fetch an account by ID.
* If the account does not exist, the service returns 404.

### Acceptance Criteria
```gherkin
Given an existing account with a known ID
When I request the account by that ID
Then the service returns 200 OK with the account details
---
