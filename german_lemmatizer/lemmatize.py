import tempfile
from pathlib import Path

import docker
from joblib import Parallel, delayed
from tqdm import tqdm

docker_image_tag = "filter/german-lemmatizer:0.5.0"

# https://stackoverflow.com/a/312464/4028896
def to_chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i : i + n]


def escape_text(text):
    return text.replace("\n", "\\n")


def unescape_text(text):
    return text.replace("\\n", "\n")


def process_chunk(c, i, working_dir, escape, remove_stop):
    with tempfile.TemporaryDirectory(
        dir=working_dir, suffix=str(i) + "_input"
    ) as input_folder:
        with tempfile.TemporaryDirectory(
            dir=working_dir, suffix=str(i) + "_output"
        ) as output_folder:
            client = docker.from_env()

            if escape:
                c = [escape_text(txt) for txt in c]

            Path(input_folder + "/data.txt").write_text("\n".join(c))

            # we need absolute path
            input_folder = str(Path(input_folder + "/").resolve())
            output_folder = str(Path(output_folder + "/").resolve())

            commands = ["--line"]

            if escape:
                commands.append("--escape")

            if remove_stop:
                commands.append("--remove_stop")

            while True:
                try:
                    client.containers.run(
                        docker_image_tag,
                        " ".join(commands),
                        volumes={
                            input_folder: {"bind": "/input", "mode": "ro"},
                            output_folder: {"bind": "/output", "mode": "rw"},
                        },
                    )
                    break
                except Exception as e:
                    print("failed, next try! " + str(e))

            with open(Path(output_folder + "/data.txt")) as output_file:
                lines = output_file.readlines()
                lines = [l.strip() for l in lines]
            if escape:
                lines = [unescape_text(txt) for txt in lines]
    return lines


def lemmatize(
    texts, chunk_size=10000, working_dir=".", escape=False, n_jobs=1, remove_stop=False
):
    # pull image if not present
    client = docker.from_env()
    images_list = sum([l.tags for l in client.images.list()], [])
    if not docker_image_tag in images_list:
        client.images.pull(docker_image_tag)

    chunks = to_chunks(texts, chunk_size)

    if n_jobs > 0:
        results = Parallel(n_jobs=n_jobs, backend="multiprocessing")(
            delayed(process_chunk)(c, i, working_dir, escape, remove_stop)
            for i, c in tqdm(enumerate(chunks), total=(len(texts) // chunk_size) + 1)
        )
    else:
        results = [
            process_chunk(c, i, working_dir, escape, remove_stop)
            for i, c in tqdm(enumerate(chunks), total=(len(texts) // chunk_size) + 1)
        ]

    for r_chunk in results:
        for r in r_chunk:
            yield r
