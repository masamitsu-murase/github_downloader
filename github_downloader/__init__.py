
import io
import pathlib
import zipfile
import requests


def _get_zip_url(github_url, hash_or_tag):
    github_url = github_url.rstrip("/")
    return github_url.rstrip("/") + ("/archive/%s.zip" % hash_or_tag)


def extract_zipped_file_with_filter(data, output_dir, filter_path):
    filter_path_split = [x for x in filter_path.split("/") if x]
    output_path = pathlib.Path(output_dir).resolve()

    with zipfile.ZipFile(io.BytesIO(data)) as file:
        for info in file.infolist():
            filename_split = info.filename.split("/")[1:]
            print(filter_path_split)
            print(filename_split)
            if filter_path_split == filename_split[:len(filter_path_split)]:
                path = output_path.joinpath(*filename_split)
                if info.is_dir():
                    path.mkdir(parents=True, exist_ok=True)
                else:
                    path.parent.mkdir(parents=True, exist_ok=True)
                    with open(path, "wb") as output:
                        output.write(file.read(info.filename))


def download_zip_with_filter(url, output_dir, filter_path=""):
    response = requests.get(url)
    if not response.ok:
        raise RuntimeError("GitHub access error: '%s': %d" % (url, response.status_code))

    extract_zipped_file_with_filter(response.content, output_dir, filter_path)


def download(github_url, relative_path=".", *, hash_or_tag="master"):
    zip_url = _get_zip_url(github_url, hash_or_tag)
    response = requests.get(zip_url)
    if not response.ok:
        raise RuntimeError("GitHub access error: '%s' %d" % (github_url, response.status_code))

    with zipfile.ZipFile(io.BytesIO(response.content)) as file:
        for info in file.infolist():
            print(info)
            filename = file.filename


url = "https://api.github.com/repos/masamitsu-murase/pausable_unittest/zipball/Ver_1_5_1"
download_zip_with_filter(url, "hogehoge")
# download(url, hash_or_tag="9e7eaf4367a7e2d8256f6b9286f71842113e27c1")
# response = requests.get(url)
# with zipfile.ZipFile(io.BytesIO(response.content)) as file:
#     for info in file.infolist():
#         print(info)
#         filename = file.filename

