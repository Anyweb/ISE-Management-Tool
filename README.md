# ISE Management Tool
A python-based tool to manage a Cisco ISE

## Usage
```bash
usage: main.py [-h] [--name NAME] [--mac MAC] [--description DESCRIPTION] [--filter-operator {EQUALS,NOT_EQUALS,STARTS_WITH,NOT_STARTS_WITH,ENDS_WITH,NOT_ENDS_WITH,CONTAINS,NOT_CONTAINS}] [--lookup] [--create] [--delete] [--delete-with-clear] [--dry-run]

🤠 ISE-Manager Light used to create, delete, search Endpoints and Endpoint Groups. And a lot more!

optional arguments:
  -h, --help            show this help message and exit
  --name NAME           Specify a name for Endpoints/Group.
  --mac MAC             Specify a MAC-Address for Endpoint.
  --description DESCRIPTION
                        Specify a Description for Endpoint/Group.
  --filter-operator {EQUALS,NOT_EQUALS,STARTS_WITH,NOT_STARTS_WITH,ENDS_WITH,NOT_ENDS_WITH,CONTAINS,NOT_CONTAINS}
                        Possible choices are: [EQUALS, NOT_EQUALS, STARTS_WITH, NOT_STARTS_WITH, ENDS_WITH, NOT_ENDS_WITH, CONTAINS, NOT_CONTAINS] Has to be used in conjunction with '--name' (for EndpointGroups) or '--mac' (for Endpoints). Defaults to
                        EQUALS.
  --lookup              🔍 [SEARCH] Find an Endpoint Group with it's Endpoints (using '--name') or an Endpoint (using '--mac'). Can be used in conjunction with '--filter-operator'
  --create              ✏️ [CREATE] Create an Endpoint Group (using '--name' and '--description') or an Endpoint (using '--mac' and '--description').
  --delete              🗑️ [DELETE] Delete an Endpoint Group (using '--name') or an Endpoint (using '--mac').
  --delete-with-clear   🗑️ [DELETE] Delete an Endpoint Group (using '--name') and all of it's Endpoints. Can be used in conjunction with '--filter-operator'.
  --dry-run             🏍️ Show what Endpoints and Groups are involved witout performing the action
  ```

# Examples

Some samples would be:   
 - Print all Endpoint Groups: `main.py --lookup --name "" --filter-operator CONTAINS`
 - Print Endpoints containing this MAC-Block: `main.py --lookup --mac "00:01" --filter-operator CONTAINS`
 - Remove (Dry-Run) Endpoint Group containing "testgb" with Endpoints:   
 ```
 /main.py --delete-with-clear --name "testgb" --filter-operator CONTAINS --dry-run
----DRY-RUN----
----------------------------------------------
 o GID: af42ae80-e5bb-11eb-894b-005056b226aa
 o Name: TestGBenAbou123
 o Description: description
  -> Endpoint: 00:01:02:03:04:06
----------------------------------------------
 o GID: 75f5ea70-e57f-11eb-894b-005056b226aa
 o Name: TestGB123
 o Description: Test Endpoint Group 1
 ```
