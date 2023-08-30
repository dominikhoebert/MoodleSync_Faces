# MoodleSync Faces

## Description

Python Script creates a Moodle XML question file using the students profile pictures of a Moodle course. A question
includes a students profile picture and 4 random answers.

## Usage

When running the main script, it is looking for a `data/credendials.json` file in the data directory.

```json
{
  "url": "https://moodle.example.com",
  "user": "username",
  "password": "password",
  "service": "ask_your_admin"
}
```

If the file is not found, the script will ask for the credentials. Ask your admin for the service name.
Then the course and a number of groups can be selected to create the questions from. The script will create one or more
XML files in the data directory, which can be imported into Moodle.

Students without a profile picture will be ignored.

## [Docker](https://hub.docker.com/repository/docker/dominik1220/moodle_sync_faces)

```bash
docker run --rm -it -v ${pwd}:/app/data dominik1220/moodle_sync_faces
```
