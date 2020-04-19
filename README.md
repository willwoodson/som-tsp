# 使用自组织映射解决旅行商问题

## 作者: Diego Vicente Martín
### EMAIL:  mail@diego.codes

该存储库包含自组织映射的实现，该映射可用于查找旅行商问题的次优解决方案。
程序支持的问题的实例是 **.tsp** 文件，这是此问题中的一种普遍格式。
所有源代码都可以在 **src** 目录中找到，而报告和简短演示幻灯片（西班牙语）可以在 **report** 文件夹中找到。
但是，要全面阅读该主题， 你可以阅读我的[博客文章](https://diego.codes/post/som-tsp/)。

![算法演示](diagrams/uruguay.gif)


要运行代码，只需要Python 3和依赖项（默认情况下包含在Anaconda发行版中的 **matplotlib**，**numpy** 和 **pandas**）。如果您不使用Anaconda，则可以使用以下命令安装所有依赖项：

```bash
pip install -r requirements.txt
```

要运行代码，只需执行以下命令：

```bash
cd som-tsp 
python src/main.py assets/<instance>.tsp
```

生成的图像将存储在**diagrams**文件夹中。
使用**convert**之类的工具，您可以通过运行以下命令轻松生成类似于此文件中的动画的动画：

```bash
cd som-tsp 
convert -delay 10 -loop 0 *.png animation.gif
```

该代码已获得MIT许可，因此可以在您的项目中随意修改和/或使用它。
如果您有任何疑问，请随时与我联系或通过创建问题来为此存储库做出贡献。

-----

该代码是针对计算机科学与技术硕士学位@ UC3M的生物启发式人工智能课程提供的。
可以在[此存储库](https://github.com/DiegoVicen/ntnu-som)中找到此代码的先前版本。
特别感谢[Leonard Kleinans](https://github.com/leo-labs)，他在之前的版本中与我合作。
