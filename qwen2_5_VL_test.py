import os
from openai import OpenAI
from PIL import ImageGrab, Image, ImageDraw
import base64
import re
import time
import json
from pynput.keyboard import Key, Controller as KeyboardController
import threading

def draw_bbox(image_path, bbox_list,txt_path,labels):
    """在图片上绘制边界框
    Args:
        image_path: 原始图片路径
        bbox_list: 边界框列表，每个边界框格式为 [x1, y1, x2, y2]
    """
    # 打开原始图片
    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)
    
    # 为每个边界框绘制矩形
    for bbox in bbox_list:
        x1, y1, x2, y2 = bbox
        # 绘制红色矩形框，线宽为3
        draw.rectangle([x1, y1, x2, y2], outline='red', width=3)
    
    # 保存标注后的图片
    output_path = 'annotated_' + os.path.basename(image_path)
    img.save(os.path.join("signed-pic",output_path))
    print(f"已保存标注图片: {output_path}")
    filename = os.path.splitext(output_path)[0]+'.txt'
    with open(os.path.join(txt_path,filename),"w",encoding='utf-8') as file:
        file.write(str(bbox_list)+str(labels))
   
   



def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def process_image(image_path, client,txt_path,object_list):
    """处理单张图片
    Args:
        image_path: 图片路径
        client: OpenAI客户端
    """
    start_time = time.time() # Start timing for single response
    print(f"\n处理图片: {image_path}")
    base64_image = encode_image(image_path)
    
    response = client.chat.completions.create(
        model="Qwen/Qwen2.5-VL-72B-Instruct",
        messages=[
            {
                "role": "system",
                "content": "你是一个视觉助手，可以帮助用户标注目标位置，构建数据集。请用JSON格式输出边界框坐标，格式为：[{\"bbox_2d\": [x1, y1, x2, y2], \"label\": \"标签(每个坐标只能有一个）\"}]，注意用户要求的的json对象个数。"
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    },
                    {
                        "type": "text",
                        "text": f"用框定位图像中{', '.join(object_list)}的位置，以数个JSON对象的格式分别输出{', '.join(object_list)}的bbox的坐标，不要输出```json```代码段"
                    }
                ]
            }
            
        ],
        stream=True,
    
    )

    # 收集完整的响应
    full_response = ""
    for chunk in response:
        if chunk.choices[0].delta.content:
            content = chunk.choices[0].delta.content
            print(content, end='', flush=True)
            full_response += content
 
            

    # 解析JSON响应并绘制边界框
    try:
        # 尝试解析JSON响应
        print(type(full_response))
        bbox_data = json.loads(full_response)
        # 提取所有边界框坐标
        bbox_list = [item['bbox_2d'] for item in bbox_data]
        labels = [item['label'] for  item in bbox_data]
        print(bbox_list)
        print(labels)
    
        # 在图片上绘制边界框
        draw_bbox(image_path, bbox_list, txt_path,labels)
    except json.JSONDecodeError:
        print("无法解析JSON响应")
    except Exception as e:
        print(f"处理过程中出现错误: {str(e)}") 
    finally:
        end_time = time.time() # End timing for single response
        time_taken = end_time - start_time
        print(f"单个响应花费时间: {time_taken:.2f} 秒")
    return time_taken

def process_folder(folder_path,txt_path,object_list):
    """处理文件夹中的所有图片
    Args:
        folder_path: 文件夹路径
    """
    # 支持的图片格式
    image_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.gif')
    total_time_spent = 0
    
    # 创建OpenAI客户端
    client = OpenAI(
        api_key="<你的API>",
        base_url="https://api.siliconflow.cn/v1"
    )
    
    # 遍历文件夹中的所有文件
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(image_extensions):
            image_path = os.path.join(folder_path, filename)
            single_response_time = process_image(image_path, client,txt_path,object_list)
            total_time_spent += single_response_time
            # 添加延时，避免请求过于频繁
            time.sleep(1)
    print(f"模型总花费时间: {total_time_spent:.2f} 秒")

if __name__ == "__main__":
    # 指定要处理的文件夹路径
    folder_path = "pic"  # 当前文件夹
    process_folder(folder_path,txt_path='txt')


