## nuScenes数据集

1. 评价指标
   
   - NDS（nuScenes）特有的评价指标 TP=True Positive
     
     > 在评测时依旧使用检测领域的AP，不过AP的阈值匹配不使用IoU来计算，而使用在<font color=red>地平面上的2D中心距离d</font>来计算。
     > 
     > 这样解耦了物体的尺寸和方向对AP计算的影响。
     > 
     > d设置为  D={0.5,1,2,4}米。在计算AP时，去除了低于0.1的recall和precision并用0来代替这些区域。
     > 
     > 不同类以及不同难度D用来计算mAP：
     > 
     >     $mAP=\frac{1}{|C||D|}\sum\limits_{c\in C}\sum\limits_{d\in D}AP_{c,d}$
     
     - $NDS = \frac{1}{10} [5\,mAP + \sum\limits_{mTP \in TP}[1- min(1, mTP)]$
   
   - 平均平移误差（ATE）——二维欧几里得中心距离
   
   - 平均尺度误差（ASE）——1-IOU， IOU为角度对其之后的三维交并比
   
   - 平均角度误差(AOE) 是预测值和真实值之间最小的偏航角差。(所有的类
     
     别角度偏差都在360∘ 内, 除了障碍物这个类别的角度偏差在180∘ 内)
   
   -  平均速度误差(AVE) 是二维速度差的L2 范数(m/s)
   
   - 平均属性错误(AAE) 被定义为1−acc, 其中acc 为类别分类准确度

2. 面临问题——长尾问题
   
   nuScenes中的不同类别数据为—— 1：10K
