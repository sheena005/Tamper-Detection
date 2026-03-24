def chunk_file(file_path, chunk_size=4096):

    chunks = []

    with open(file_path, "rb") as f:
        while True:
            data = f.read(chunk_size)

            if not data:
                break

            chunks.append(data)

    return chunks