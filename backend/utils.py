
async def save_uploaded_file(file, destination: str = "C:/Users/shbhm/Downloads/llm-assignment-master/llm-assignment-master/backend/assets"):
    file_path = f"{destination}/{file.filename}"
    with open(file_path, "wb") as new_file:
        new_file.write(await file.read())
    return file_path
