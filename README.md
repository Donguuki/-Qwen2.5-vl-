
1.  **准备环境**:
    *   确保已安装Python环境。
    *   安装必要的Python库，包括PyQt5，OpenAI客户端库，Pillow (PIL)。
    *   获取一个有效的OpenAI API Key，并在`qwen2_5_VL_test.py`中配置`client`的`api_key`和`base_url`。
2.  **组织实验数据**:
    *   创建或指定一个文件夹，例如`pic`，将所有待标注的图片放入其中。
    *   （可选）运行`rename_pic.py`脚本对图片进行统一重命名。
3.  **启动标注工具**:
    *   运行`gui_client.py`脚本，启动图形用户界面。
4.  **选择图片文件夹**:
    *   在GUI界面中，点击"浏览..."按钮，选择包含实验数据的图片文件夹。
5.  **输入待标注物体**:
    *   在"输入需要标注的物体"文本框中，输入需要模型识别并标注的物体名称，多个物体之间用逗号分隔（例如："冰人,火人,蓝色钻石"）。
6.  **开始处理**:
    *   点击"开始处理"按钮。工具将启动一个后台线程，逐一处理文件夹中的图片。
7.  **查看日志和结果**:
    *   在GUI的"运行日志"区域，可以实时查看图片处理的进度和任何错误信息。
    *   处理完成后，标注后的图片将保存在`signed-pic`文件夹中，对应的边界框数据将保存在`txt`文件夹中的`.txt`文件中。


*   **视觉标注结果**: 在`signed-pic`文件夹中生成的`annotated_*.png`（或其他图片格式）文件，这些文件直观地展示了模型在原始图片上识别并绘制出的边界框。通过观察这些图片，可以评估模型的识别准确性和边界框的精确度。例如，如果模型成功识别出"冰人"并准确地用红色框将其包围，则表明模型在该物体上的性能良好。

*   **结构化数据结果**: 在`txt`文件夹中生成的`.txt`文件，每个文件对应一张图片，其中包含了JSON格式的边界框坐标和标签信息。这些数据是构建机器学习数据集的关键。例如，一个`txt`文件可能包含`[[x1, y1, x2, y2], [x3, y3, x4, y4]]['冰人','火人']`这样的信息，表示图片中"冰人"和"火人"的位置。通过分析这些文本文件，可以进行数据清洗、格式转换，并用于训练目标检测模型。
