# 使用自组织映射(SOM)解决旅行商问题

## 作者: 李志
### EMAIL:  201782016@mail.dlut.edu.cn

## 1. 简介

该存储库包含 **标准som** (Self-Organizing Maps)及其改进版本 **orc_som** (Overall-Regional Competitive Self-Organizing Maps)和 **orcts_som** (Overall-Regional Competitive & tabu search Self-Organizing Maps)
的实现。

自组织映射 (Self-Organizing Maps) 是一种*无监督的聚类方法*，可用于查找旅行商问题的次优解决方案。SOM通过模拟人脑神经元的自组织和侧抑制现象，在训练中逐渐学习到城市空间位置关系，最终输出一个环形的神经元结构用于描述最优路径。


## 2. 算法演示

![算法演示](report/som.gif)

### 文件夹内容说明
```bash
├─assets            描述旅行商问题的 .tsp 文件
├─data
│  ├─cities         读取到的城市坐标             
│  ├─process        神经网络训练过程
│  └─routes         最优路径
├─report            算法对比分析报告               
└─src
   └─library
       ├─orcts_som  泛化竞争&全局渗透&禁忌搜索 som 类
       ├─orc_som    泛化竞争&全局渗透 som 类
       └─som        标准 som 类   
```

各算法对于解决不同Tsp问题的优劣表现

| n   |      tsp      | optimal_solution |       som | orc_som | orcts_som |
| --- | :-----------: | :--------------: | --------: | ------: | --------: |
| 0   |     st70      |      675.0       |     3.03% |   2.91% | **1.97%** |
| 1   |     pr76      |     108159.0     | **2.19%** |   3.65% |     2.73% |
| 2   |     rat99     |      1211.0      |     6.36% |   4.91% | **4.51%** |
| 3   |     ch130     |      6110.0      | **2.47%** |   3.07% |     4.07% |
| 4   |    kroA200    |     29368.0      |     4.24% |   4.14% | **3.94%** |
|     | ***average*** |                  |     3.65% |   3.74% | **3.43%** |

## 3. 使用说明

要运行代码，只需要Python 3和依赖项（ **matplotlib**，**numpy** 和 **pandas**）。如果您还未安装，则可以使用以下命令安装所有依赖项：

```bash
pip install -r requirements.txt
```

要运行代码，只需执行以下命令：

```bash
cd som-tsp 
python src/main.py assets/<instance>.tsp
```

som网络训练过程可视化，可查看图片 **data/som.png**，训练过程以.png图片和.gif动态图片的形式存储在 **data/process** 下的相应Tsp问题名文件夹中，算法最终生成的路径将存储在 **data/routes** 文件夹中。

## 4. 其他功能简介

可以在src/main.py中注释相关代码，来选择不同的算法

```python
from library.som.som_tsp import SomTsp
from library.orc_som.som_tsp import SomTsp
from library.orcts_som.som_tsp import SomTsp
```

直接运行src/analyze.py，可以多批次 (*step_num*) 分析不同算法（方法同上）对于解决不同Tsp问题 (*tsp_name*) 的优劣表现。

```python
step_num = 5
tsp_name = ["st70", "pr76", "rat99", "ch130", "kroA200"]
```

运行结果会在终端输出，并保存在 **data/record.csv** 中，内容如下：
| n   |   tsp   | optimal_solution |   step1   |   step2   |   step3   |   step4   |   step5   |  average   | deviation |
| --- | :-----: | :--------------: | :-------: | :-------: | :-------: | :-------: | :-------: | :--------: | --------: |
| 0   |  st70   |      675.0       |  685.90   |  701.94   |  702.87   |  692.31   |  694.61   |  695.526   |     3.04% |
| 1   |  pr76   |     108159.0     | 113017.14 | 113986.81 | 113034.70 | 113648.07 | 112306.07 | 113198.558 |     4.66% |
| 2   |  rat99  |      1211.0      |  1291.71  |  1234.96  |  1265.81  |  1264.23  |  1302.83  |  1271.908  |     5.03% |
| 3   |  ch130  |      6110.0      |  6385.14  |  6491.81  |  6462.22  |  6376.38  |  6258.89  |  6394.888  |     4.66% |
| 4   | kroA200 |     29368.0      | 30617.66  | 30423.39  | 30497.94  | 30889.82  | 30589.94  | 30603.750  |     4.21% |


如果您有任何疑问，请随时与我联系或通过创建问题来为此存储库做出贡献。

-----

该代码是用于本人现代智能优化算法课设，
部分代码借鉴[此存储库](https://github.com/DiegoVicen/som-tsp)

