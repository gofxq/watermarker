import exifread

def read_exif(file_path):
    with open(file_path, 'rb') as f:
        tags = exifread.process_file(f)

    for tag in tags.keys():
        print(f"{tag}: {tags[tag]}")

# 示例：读取 Sony 相机的 ARW 文件
file_path = 'lighted_cloud.ARW'
read_exif(file_path)
