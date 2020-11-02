## Getting Started

- Clone this repository and cd into the code folder
    ```
    git clone git@source.datanerd.us:jhagan/nr-usr-mgr.git
    cd nr-usr-mgr
    ```
- Make sure you have Python 3 installed and then build your virtual environment and install your dependencies
    ```
    virtualenv venv
    . ./venv/bin/activate
    pip install -r requirements.txt
    ```

If python 3 is not the default Python in your environment virtualenv will allow you to specify a specific version of python like so:

```
 virtualenv --python=/usr/bin/python3 <path/to/myvirtualenv>
```

- Run the test command and evaluate your outputs
    ```
    python nr-user-mgr.py test-conf.yaml
    ```

- Based on the test config file this run will ingest a file named `test-users.csv` and output too new files: `test-users-modify.csv` and `test-users-purge.csv`.   The input is of a format generated by our `bulk actions` page in the New Relic user manager.  The output files can be used with the `update` and `delete` actions respectively.


## Sample Input File Data

```
Email,Name,User type,Base role,Add-on roles,Last active
igor.smith@acme.com,Igor Smith,full,user,,
mike.jones@acme.com,Mike Jones,full,user,"apm_admin,alerts_admin,infrastructure_admin,synthetics_admin,mobile_admin,browser_admin,insights_admin","Nov 10, 2018 1:29:14 pm"
santosh.kumar@acme.com,Santosh Kumar,full,user,"apm_admin,alerts_admin,infrastructure_admin,synthetics_admin,mobile_admin,browser_admin,insights_admin","Jan 8, 2019 9:28:49 am"
jose.cruz@acme.com,Jose Cruz,full,admin,,"Apr 15, 2019 2:00:58 pm"
jim.johnson@acme.com,Jim Johnson,full,admin,,"Mar 20, 2019 12:35:17 pm"
mark.evans@acme.com,Mark Evans,full,admin,,"Sep 11, 2020 6:50:04 pm"
matthew.manfredonia@acme.com,"Matt ",full,admin,,"Dec 18, 2019 5:00:12 pm"
```

## Sample Output File Data

The output files will be identical in format to the input file structure except the program will add to additional fields: *change* and *change_reason*

Valid change/change_reason pairs are:

| change     | change_reason  |
|------------|----------------|
| UPGRADE    | FORCE_ALL      |
| DOWNGRADE  | FORCE_ALL      |
| UPGRADE    | UPGRADE_LIST   |
| DOWNGRADE  | DOWNGRADE_LIST |
| PURGE      | PURGE_LIST     |
| PURGE      | NEVER_ACTIVE   |
| PURGE      | PENDING        |
| DOWNGRADE  | INACTIVE_TIME  |

The `modify` file will contain various changes to the user type based on the configuration in the yaml file.  This file can be used with the update bulk action in RPM.

```
Email,Name,User type,Base role,Add-on roles,Last active,change,change_reason
mike.jones@acme.com,Mike Jones,basic,user,"apm_admin,alerts_admin,infrastructure_admin,synthetics_admin,mobile_admin,browser_admin,insights_admin","Nov 10, 2018 1:29:14 pm",DOWNGRADE,INACTIVE_TIME
santosh.kumar@acme.com,Santosh Kumar,basic,user,"apm_admin,alerts_admin,infrastructure_admin,synthetics_admin,mobile_admin,browser_admin,insights_admin","Jan 8, 2019 9:28:49 am",DOWNGRADE,INACTIVE_TIME
jose.cruz@acme.com,Jose Cruz,basic,admin,,"Apr 15, 2019 2:00:58 pm",DOWNGRADE,INACTIVE_TIME
jim.johnson@acme.com,Jim Johnson,basic,admin,,"Mar 20, 2019 12:35:17 pm",DOWNGRADE,INACTIVE_TIME
matthew.manfredonia@acme.com,Matt ,basic,admin,,"Dec 18, 2019 5:00:12 pm",DOWNGRADE,INACTIVE_TIME
Krishna.Reddy@acme.com,Krishna ,basic,admin,,"May 1, 2019 11:20:51 am",DOWNGRADE,INACTIVE_TIME
april.rathe@acme.com,april rathe,basic,user,"apm_admin,alerts_admin,infrastructure_admin,synthetics_admin,mobile_admin,browser_admin,insights_admin","Sep 19, 2018 7:56:10 am",DOWNGRADE,INACTIVE_TIME
Anatolii.Perekhodko@acme.com,Anatolii Perekhodko,basic,user,"apm_admin,alerts_admin,infrastructure_admin,synthetics_admin,mobile_admin,browser_admin,insights_admin","Apr 9, 2020 11:13:15 am",DOWNGRADE,INACTIVE_TIME
```

Users that meet any of the `PURGE` criteria will end up in the `purge` file which can be used with the delete bulk action in RPM.

```
Email,Name,User type,Base role,Add-on roles,Last active,change,change_reason
igor.smith@acme.com,Igor Smith,full,user,,,PURGE,NEVER_ACTIVE
Pam.Mantri@acme.com,p******* m*******,full,user,,,PURGE,NEVER_ACTIVE
Prakash.Kumar@acme.com,P******* K*******,full,user,"apm_admin,alerts_admin,infrastructure_admin,synthetics_admin,mobile_admin,browser_admin,insights_admin",,PURGE,NEVER_ACTIVE
Ioana.Potinteu@acme.com,I******* P*******,full,user,,,PURGE,NEVER_ACTIVE
Nitin.Bhole@acme.com,N******* B*******,full,user,,,PURGE,NEVER_ACTIVE
Milind.Gogate@acme.com,M******* G*******,full,user,,,PURGE,NEVER_ACTIVE
Wei.Cheng@acme.com,W******* C*******,full,user,,,PURGE,NEVER_ACTIVE
Yuhui.Ouyang@acme.com,Y******* O*******,full,user,,,PURGE,NEVER_ACTIVE
Alexandru.Craciun@acme.com,A******* C*******,full,user,,,PURGE,NEVER_ACTIVE
Marius.Popa@acme.com,M******* P*******,full,user,,,PURGE,NEVER_ACTIVE
Vlad.Dragan@acme.com,V******* D*******,full,user,,,PURGE,NEVER_ACTIVE
Jeremy.Gabalski@acme.com,J******* G*******,full,user,,,PURGE,NEVER_ACTIVE
Ritesh.Gupta@acme.com,R******* G*******,full,user,,,PURGE,NEVER_ACTIVE
Alexandru.Peptan@acme.com,A******* P*******,full,user,,,PURGE,NEVER_ACTIVE
Andreea.Meirosu@acme.com,A******* M*******,full,user,,,PURGE,NEVER_ACTIVE
Andras.Szekely@acme.com,A******* S*******,full,user,,,PURGE,NEVER_ACTIVE
Costel.Dragu@acme.com,C******* D*******,full,user,,,PURGE,NEVER_ACTIVE
Carmichael.Ragbir@acme.com,C******* R*******,full,user,,,PURGE,NEVER_ACTIVE
kwood@aqrcapital.com,K******* W*******,full,user,,Pending,PURGE,PENDING
```

## Sample Config File

```
infile: 'test-users.csv'
downgradable_inactivity_days: 60
purge_never_active_accounts: true
purge_pending_accounts: true
force_purge_user_list:
  - "Kailash.Raythour@acme.com"
force_upgrade_user_list:
  - "Mike.O'Rourke@acme.com"
force_downgrade_user_list:
  - "Eli.Weg@acme.com"
force_upgrade_all_users: false
force_downgrade_all_users: false
```

### Config parameters and meaning


| parameter                    | type           | description                                                             |
|------------------------------|----------------|-------------------------------------------------------------------------|
| infile                       | string         | CSV file generated from the RPM bulk actions page.                      |
| downgradable_inactivity_days | integer        | If inactive greater than this will be downgraded to "basic"             |
| purge_never_active_accounts  | boolean        | If they have never been active purge them                               |
| purge_pending_accounts       | boolean        | Purge accounts with last active set to "Pending"                        |
| downgrade_never_active_accounts  | boolean        | If they have never been active downgrade them                               |
| downgrade_pending_accounts       | boolean        | Downgrade accounts with last active set to "Pending"                        |
| force_purge_user_list        | list of string | list of emails of users who will be force purged use (`[]` for empty).  |
| force_upgrade_user_list      | list of string | list of emails of users who will be force upgraded (use `[]` for empty) |
| force_downgrade_user_list    | list of string | list of user emails who will be force downgraded (use `[]` for empty)   |
| force_upgrade_all_users      | boolean        | upgrades all users to "full"                                            |
| force_downgrade_all_users    | boolean        | downgrades all users to "basic"                                         |

### Future config parameters (not currently supported)

| parameter                      | type   | description                                                          |
|--------------------------------|--------|----------------------------------------------------------------------|
| external_activity_csv          | string | name of external file with user last active dates (i.e., from Helix) |
| external_activity_active_field_name | string | the field to use from the external activity file|
| external_activity_active_field_dateformat | string | dateformat for `strptime` to use for parsing default is: `"%b %d, %Y %H:%M:%S %p"`|           |