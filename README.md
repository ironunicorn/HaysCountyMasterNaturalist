# Hays County Master Naturalist Volunteer, Advanced Training, and Events App

## To build vue app

```sh
cd opportunities
```

```sh
npm run build
```

Add generated .js and .css filenames to flaskapp/VolunteerAT/templates/opportunities/index.html and .css filename to flaskapp/VolunteerAT/templates/base.html

At some point I might automate this and make it less painful for development.

## To run flask app locally
- Be sure you have MySQL installed and running.
- Create an `hcmn` database.
- Edit credentials in the `get_db` function as needed in flaskapp/VolunteerAT/db.py
- Create virtual env if desired.

```sh
cd flaskapp
```

```sh
pip install -r requirements.txt
```

```sh
flask --app VolunteerAT init-db
```

```sh
flask --app VolunteerAT run
```

## To run flask app in production
Be sure to set the following environmental variables:
- SECRET_KEY
- DATABASE_URL
- DATABASE_NAME
- DATABASE_USER
- DATABASE_PASSWORD
