# 单目跨视角的道路场景估计

借鉴：<font color=red>单目BEV——可以作为比较对象</font>

![](/home/yihang/.config/marktext/images/2022-07-26-10-54-57-2022-07-26%2010-54-31%20的屏幕截图.png)

| Title              | Projecting Your View Attentively: Monocular Road Scene Layout Estimation via Cross-view Transformation |
| ------------------ | ------------------------------------------------------------------------------------------------------ |
| Athour             | Weixiang Yang1,Qi Li1,Wenxi Liu1∗,Yuanlong Yu1∗,Yuexin Ma2,3,Shengfeng He4,Jia Pan5                    |
| Conference/Journal | CVPR2021                                                                                               |
| Contributes        | 1. 单GPU上达到35 FPS， 能实时的对HD地图重建<br/>2. 场景感知器能考虑到车辆和道路的空间信息                                               |

- 针对Lidar设备贵， 以及处理耗时问题提出
- 任务：道路布局估计 和 车辆占用（车流）估计——<font color=red>如何用到3D 目标检测中</font>

##### 模型架构

![](/home/yihang/.config/marktext/images/2022-07-26-11-30-26-2022-07-26%2011-30-08%20的屏幕截图.png)

具体操作：

- 采用ResNet作为Encoder, 编码特征

- cross-view transformer增强视图投影的特征

- Cycled View Projection(CVP)——解决特征空间对齐问题， 采用FC层，更能结合全局特征

- CVP 主要是 通过 self supervised的方法 确保 投影的 有效性

- Key =X , Query = $X^{\prime}$, Value = $X^{\prime \prime}$
  
   

##### CVT结构

![](/home/yihang/.config/marktext/images/2022-07-26-11-45-26-2022-07-26%2011-44-51%20的屏幕截图.png)

##### BEV借鉴的点

实验结果

![](/home/yihang/.config/marktext/images/2022-07-26-14-07-05-2022-07-26%2014-06-51%20的屏幕截图.png)

![](/home/yihang/.config/marktext/images/2022-07-26-14-03-10-2022-07-26%2014-02-49%20的屏幕截图.png)

1. CVP中的自注意力结构  Cycle Struture（效果不明显）

2. Cross-view correlation (效果明显)， 使用QKV

3. 可能只是 <font color=red>Transformer的效果</font>？？

    MonoLayout的网络结构：

    ![](/home/yihang/.config/marktext/images/2022-07-26-14-11-06-2022-07-26%2014-10-34%20的屏幕截图.png)

4. CVT中的 Feature Selection 提升效果能达到3%~4%。对$X^{\prime}$ 和$X^{\prime \prime}$进行了 融合。但是 生成Value 的思想可以。












