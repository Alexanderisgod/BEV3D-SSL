#### Lift-Splat

![](/home/yihang/.config/marktext/images/2022-07-27-09-57-23-2022-07-27%2009-56-57%20的屏幕截图.png)

| Title              | Lift, Splat, Shoot: Encoding Images from Arbitrary Camera Rigs by Implicitly Unprojecting to 3D |
| ------------------ | ----------------------------------------------------------------------------------------------- |
| Athour             | Jonah Philion, Sanja Fidler NVIDIA, Vector Institute, University of Toronto                     |
| Conference/Journal | ECCV 2020                                                                                       |
| Arxiv              | https://arxiv.org/abs/2008.05711                                                                |
| Github             | https://github.com/nv-tlabs/lift-splat-shoot                                                    |

- 显式地建立了Camera view到BEV空间的特征映射

##### 模型结构

![](/home/yihang/.config/marktext/images/2022-07-27-10-09-42-2022-07-27%2010-09-20%20的屏幕截图.png)

get_geometry：create_frustum其实是对 camera图像进行间隔取点， 获取 三维坐标。然后， 将 Camera 像素 （x, y, z）对应在 自车坐标系中的3D坐标

->[B, N, 512, H//downsample, W//downsample, 3] 。 <mark>目的：</mark> 将每个Camera的3D点投影到 ego 坐标系。

CamEncode： 对Backbone提取的特征进行 维度变换（D+C）， D为预测的3D空间的可选深度，C为特征维度， 然后 D$\times$ C 获得了2D图像 估计得到的3D空间特征。->[B, N, C, D, H//downsample, W//downsample]

voxel_pooling：

    input:  

        每个camera的对应的 3D点->geom_features,    x->每个相机的feature map

将相机中对应的 3D特征 投影到 BEV视角下的2D平面（首先需要过滤其中的超出自车BEV观测范围[200, 200]）。->[B, C(default=512), N_z, N_x, N_y]

```text
# 将所有的feature基于坐标位置进行排序，在俯视图上相同坐标的feature的ranks值相同
        ranks = geom_feats[:, 0] * (self.nx[1] * self.nx[2] * B)\
            + geom_feats[:, 1] * (self.nx[2] * B)\
            + geom_feats[:, 2] * B\
            + geom_feats[:, 3]
```

 排序可能出现问题：不同camera view， 甚至不同的 batch 都可能出现 小概率的特征混淆。

BevEncode：对voxel_pooling的特征进行BEV编码， 采用resnet18.

---

#### BEVDet

BEVDet主要是在lift splat上加上了 检测头

![](/home/yihang/.config/marktext/images/2022-07-27-13-06-27-2022-07-27%2013-06-11%20的屏幕截图.png)

| Title  | BEVDet: High-Performance Multi-Camera 3D Object Detection in Bird-Eye-View |
| ------ | -------------------------------------------------------------------------- |
| Athour | Junjie Huang , Guan Huang, Zheng Zhu, Yun Ye, and Dalong Du                |
| Arxiv  | https://arxiv.org/pdf/2112.11790v1.pdf                                     |
| Github | https://github.com/HuangJunJie2017/BEVDet                                  |

##### 模型结构

- Image-view Encoder
  
  - backbone：使用 resnet 或 SwinTransformer
  
  - FPN-LSS

- View Transformer（集成 LSS 的 view transformer）
  
  - 基于图像特征预测 depth
  
  - 基于预测的 depth 和 图像特征 render 点云
  
  - 竖直方向上做 pooling 得到 BEV 特征

- BEV Encoder
  
  - resnet + FPN-LSS
  
  - task-specific head，这里复用 CenterPoint 的 head

##### 思考

- 主要是替换了 特征提取的 BackBone， 同时在Image-view和BEV encoder上都加入了FPN的结构， 用于融合特征

- 主体结构和Lift, Splat没有什么变化

- 根据任务的目标， 加入了head（[CenterPoint](https://github.com/tianweiy/CenterPoint/blob/master/det3d/models/bbox_heads/center_head.py)）

- <mark>后处理</mark>采用了 Scale-NMS， 针对的问题——BEV视角下的 IOU会变小， 如行人和交通灯（不满足最小的BEV分辨率0.8m）。本文会根据 种类 缩放 物体， 即是对不同的物体施加 更高的注意力。

##### 结果分析

![](/home/yihang/.config/marktext/images/2022-07-27-13-33-33-2022-07-27%2013-33-02%20的屏幕截图.png)

    <mark>引申：</mark> 数据增强很重要， 那这是怎么起作用的？？

    Image View中使用 变换矩阵A， 然后在view transformer中， 反变换回去， 能保持空间一致性

    BEV空间：like flipping, scaling, and rotating，用在了view transformer输出的特征， 以及 需要预测的3D物体框。

---

#### BEVDet4D

    BEVDet上融合了 加入时间约束

| Title  | BEVDet4D: Exploit Temporal Cues in Multi-camera 3D Object Detection |
| ------ | ------------------------------------------------------------------- |
| Athour | Junjie Huang , Guan Huang                                           |
| Arxiv  | https://arxiv.org/pdf/2203.17054v3.pdf                              |
| Github | https://github.com/HuangJunJie2017/BEVDet                           |

##### 模型结构

![](/home/yihang/.config/marktext/images/2022-07-27-13-35-52-2022-07-27%2013-35-42%20的屏幕截图.png)

- 提取了$t-1, t, t+1$ 3帧的特征

- 经过view transformer

- Extra BEV Encoder对 不同帧的时间特征进行对齐

- 先Align特征， 并对特征进行过滤，然后 输入BEV Encoder 获得BEV特征， 经由head预测

##### 思考

- 如何 对其不同帧 之间的特征， 不同帧之间， 存在自车的运动， 用在single camera怎么样？？不同视角相机 （front, front-left， back...）的自车运动影响怎么消除？
  
  ![](/home/yihang/.config/marktext/images/2022-07-27-14-37-29-2022-07-27%2014-36-57%20的屏幕截图.png)

- 估计的准确吗？？影响大不大？？只能针对 同一scene的物体进行预测吗， 还是多少帧 图像， 能学到自车的运动？

- 或者直接估计自车的速度， 能不能更有效果
