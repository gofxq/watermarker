import rawpy
from PIL import Image, ImageDraw, ImageFont
import exifread

def extract_exif_info(file_path):
    with open(file_path, 'rb') as f:
        tags = exifread.process_file(f)
    
    # 提取关键信息（可根据需要调整）
    exif_info = {
        "Camera": tags.get("Image Model", "N/A"),
        "Lens": tags.get("EXIF LensModel", "N/A"),
        "Exposure Time": tags.get("EXIF ExposureTime", "N/A"),
        "F-Number": tags.get("EXIF FNumber", "N/A"),
        "ISO": tags.get("EXIF ISOSpeedRatings", "N/A"),
        "Date": tags.get("EXIF DateTimeOriginal", "N/A"),
    }
    
    return exif_info

def convert_arw_to_png(arw_file_path, output_png_path):
    # 使用 rawpy 读取 ARW 文件
    with rawpy.imread(arw_file_path) as raw:
        rgb_image = raw.postprocess()

    # 转换为 PIL 图像
    image = Image.fromarray(rgb_image)

    # 保存为高质量的PNG格式
    image.save(output_png_path, "PNG", quality=95)

    return output_png_path

def add_watermark(image_path, exif_info, output_path):
    # 打开PNG文件
    image = Image.open(image_path)

    # 使用Pillow的默认字体
    font = ImageFont.load_default()
    draw = ImageDraw.Draw(image)
    
    # 计算字体大小为图片高度的1%
    font_size = int(image_height * 0.01)
    
    # 准备水印文本
    watermark_text = "\n".join([f"{key}: {value}" for key, value in exif_info.items()])

    # 获取文本边界框
    text_bbox = draw.textbbox((0, 0), watermark_text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    image_width, image_height = image.size

    # 计算文本的位置（右下角）
    x = image_width - text_width - 20
    y = image_height - text_height - 20

    # 添加水印
    draw.text((x, y), watermark_text, font=font, fill=(255, 255, 255, 128))  # 白色半透明

    # 保存为高质量的PNG格式
    image.save(output_path, "PNG", quality=95)

def process_arw_and_add_watermark(arw_file_path, final_output_path):
    # 临时PNG文件路径
    temp_png_path = 'temp_image.png'
    
    # 步骤1: 转换 ARW 文件为 PNG
    png_file_path = convert_arw_to_png(arw_file_path, temp_png_path)
    
    # 提取 EXIF 信息
    exif_info = extract_exif_info(arw_file_path)
    
    # 步骤2: 添加水印到 PNG 文件
    add_watermark(png_file_path, exif_info, final_output_path)

    # 删除临时文件（可选）
    # os.remove(temp_png_path)

# 示例使用
arw_file_path = 'lighted_cloud.ARW'  # 替换为你的ARW文件路径
final_output_path = 'final_output_image.png'

process_arw_and_add_watermark(arw_file_path, final_output_path)
