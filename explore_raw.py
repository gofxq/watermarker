import rawpy

def explore_metadata(input_path):
    with rawpy.imread(input_path) as raw:
        for attribute in dir(raw):
            # Use a try-except block to handle any exceptions when accessing properties
            try:
                value = getattr(raw, attribute)
                if not callable(value):
                    print(f"{attribute}: {value}")
            except Exception as e:
                print(f"{attribute}: Could not retrieve value. Error: {e}")

# Call this function with the path to your ARW file
# explore_metadata('lighted_cloud.ARW')

import pyexiv2

def read_exif_from_arw(file_path):
    # 使用pyexiv2打开ARW文件
    metadata = pyexiv2.Image(file_path)
    
    # 读取EXIF数据
    exif_data = metadata.read_exif()

    # 打印所有的EXIF信息
    for key, value in exif_data.items():
        print(f"{key}: {value}")

# 使用示例
read_exif_from_arw("lighted_cloud.ARW")


