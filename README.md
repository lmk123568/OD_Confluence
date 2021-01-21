# OD Confluence

目标检测中替代传统NMS的后处理方式，个人简单复现，原作作者暂时还没开源

<img src="md\11.png" alt="11" style="zoom:50%;" />

<img src="md\12.png" alt="12" style="zoom:50%;" />



------

![1](\md\1.png)

paper：https://arxiv.org/abs/2012.00257

## Introduction

<img src="md\2.png" alt="2" style="zoom:75%;" />

​	本文提出了一种在目标检测中的边界框选择和抑制任务中替代 NMS 的新颖方法。它提出了Confluence，一种不仅仅依赖于 confidence scores 来选择最佳边界框的算法，也不依赖于 IoU 来消除误报。使用“曼哈顿距离”，它选择最接近群集中其他所有边界框的边界框，并删除高度融合的相邻框。因此，Confluence基于与Greedy  NMS及其变体根本不同的理论原理，代表着边界框选择和抑制的范式转变。使用MS COCO和PASCAL VOC  2007数据集，在RetinaNet，YOLOv3和Mask-RCNN上对融合进行了实验验证。使用具有挑战性的 0.50:0.95  mAP评估指标，汇合在两个mAP上均优于Greedy  NMS，并且在两个数据集上的召回率均优于。在每个检测器和数据集上，mAP改善了0.3-0.7％，而召回率则提高了1.4-2.5％。提供了Greedy  NMS和Confluence算法的理论比较，并通过广泛的定性结果分析来支持定量结果。此外，跨mAP阈值的灵敏度分析实验支持以下结论：Confluence比NMS更可靠。

## Methodology

曼哈顿距离：

![3](\md\3.png)

任意两个边界框接近度P：

![4](\md\4.png)

如图所示：

<img src="\md\5.png" alt="5" style="zoom:80%;" />

实际上对象及其相应边界框具有不同大小，需要进一步Normalization

<img src="md\6.png" alt="6"  />

伪代码：

![7](\md\7.png)

设集合B：一个class下所有bbox，集合C：提取的最终bbox

1. 提取一个class的所有bbox
2. 对所有bbox的每个bbox，计算这个bbox与其他bbox的P
   1. P<2的bbox与原bbox一起看作cluster
   2. 在这cluster计算WP
   3. 选取这个bbox最小的WP
3. 从B中选出具有最小的WP的bbox，将这个提取的bbox加入C，同时从B中删除这个bbox属于的cluster中所有bbox
4. 重复迭代上述过程，直到集合B为0



## Results

![8](md\8.png)

