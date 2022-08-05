### Optimizer

#### Warm-up

---

#### LARS ：Layer-wise Adaptive Rate Scaling

参考 |  https://www.jianshu.com/p/e430620d3acf

##### 出发点

常用的对抗网络，采用大的Batch Size在多GPU训练，但是会增加训练Epoch，所以常增大LR的方式缓解；然而， LR增大会使得学习不稳定， 所以提出了Warm-up的方式， 在$t$ epoch时，缓慢增加到 一定的LR（通常和Batch size的 expand ration采用linear scale rule）

##### 方法

网络的更新公式$w_{t+1}=w_t-\lambda\bigtriangledown L(w_t) $ 观察到网络不同Layer的   $ratio=\frac{||w_t||}{\bigtriangledown||w_t||}$， 差异很大。如果在学习的早期阶段学习率太大的话，对某些ratio较小的层，可能存在$\lambda\bigtriangledown L(w_t)$ 的值大于权重$w_t$ ，而造成训练不稳定。

既然并不是所有层的ratio比较小，那么各个层的更新参数使用的学习率应该根据自己的情况有所调整，而不是所有层使用相同的学习率。由此，作者引入了局部学习率（local LR）的概念，从而在全局学习率的基础上根据每层的情况进行适当地调整。局部学习率的计算方式:

$$
\lambda^l=\eta * \frac{||w^l||}{||\bigtriangledown L(w^l)||}
$$

![](https://upload-images.jianshu.io/upload_images/18299912-b6515515a8fb9e4c.png?imageMogr2/auto-orient/strip|imageView2/2/w/772/format/webp)

作用：工程上， 可以通过增加 GPU的方式，进行 big batch size训练，而且model performence 能保持不衰减，能节省模型训练时间，加快项目研发进度。

##### 缺陷

1. 本方法对超参 $\eta$ 敏感

2. 实验对比不全面，LARS的提出是为了替代warm-up策略，但是在ImageNet数据集上，作者只给出了warm-up+LARS的实验效果，不得不让人怀疑该方法的广泛有效性。

3. 本文超参太多了，感觉很trick

---

#### Ranger

#### 
