import os
from PIL import Image, ImageDraw, ImageFont
import exiftool

def add_watermark(photo_path, watermark_text):
    # 使用exiftool读取照片的元数据
    with exiftool.ExifTool() as et:
        metadata = et.get_metadata(photo_path)

    # 打开照片
    image = Image.open(photo_path)
    width, height = image.size

    # 创建一个用于绘画的对象
    draw = ImageDraw.Draw(image)

    # 设置字体和字体大小（确保有这个字体文件，或者更换为系统中有的字体）
    font = ImageFont.truetype('Arial.ttf', 36)

    # 在右下角添加水印
    text_width, text_height = draw.textsize(watermark_text, font=font)
    x = width - text_width - 10
    y = height - text_height - 10
    draw.text((x, y), watermark_text, font=font, fill=(255, 255, 255))

    # 附加一些拍摄信息，例如ISO
    iso = metadata.get('EXIF:ISO', 'Unknown ISO')
    draw.text((10, 10), f'ISO: {iso}', font=font, fill=(255, 255, 255))

    # 保存修改后的图片
    image.save('watermarked_image.jpg')

# 使用示例
add_watermark('lighted_cloud.ARW', 'gofxq')
