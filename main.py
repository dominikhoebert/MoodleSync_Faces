from moodle_sync_faces import MoodleSyncFaces
from face import save_faces_json

# credentials_file = "data/credentials_local.json"
credentials_file = "data/credentials.json"
faces_path = "data/faces/3AHIT/"
faces_json = "data/faces.json"


def main():
    ms = MoodleSyncFaces.from_json(credentials_file)
    ms.load_courses()
    print(ms.courses)
    ms.get_groups_of_course(ms.courses[0])
    print(ms.courses[0].groups)
    faces = ms.get_faces(ms.courses[0], ms.courses[0].groups[0])
    successful_downloads = ms.download_faces(faces, path=faces_path)
    print(f"{successful_downloads}/{len(faces)} faces downloaded successfully.")
    save_faces_json(faces, filename=faces_json)
    print(faces)


if __name__ == "__main__":
    main()
