## 半监督学习

### 一致性正则

定义：要求一个模型对相似的输入有相似的输出，即输入数据注入噪声，模型输入也不变，鲁棒性。

参考 

- [【半监督学习】Π-Model、Temporal Ensembling、Mean Teacher - wuliytTaotao - 博客园](https://www.cnblogs.com/wuliytTaotao/p/12825797.html)

- https://zhuanlan.zhihu.com/p/526985640

| 模型                  | 特点                                                                                                       | 结构图                                                                                                                              |
| ------------------- | -------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| Π 模型                | 同一有标记$x^1$和无标记的$x^2$ 经过（数据增强和dropout），计算$f(x^1)和f(x^2)$的差距+$f(x^1)和y$ 的差距                                | <img src="https://img2020.cnblogs.com/blog/1351564/202006/1351564-20200609091901374-2059403596.png" title="" alt="" width="318"> |
| Temporal Ensembling | 同Π 模型相比， 将$f(x^2)$ 替换为$Ensemble[\sum_{1}^{n}f_{epoch-1}(x^i)]$ ， 使得 $\widetilde z_i$  每个epoch后才更新，大型数据集慢 | ![](https://img2020.cnblogs.com/blog/1351564/202006/1351564-20200609091937752-414637732.png)                                     |
| Mean Teacher        | 认为Temporal Ensembling 进行EMA效果并不好，相较于前者对预测进行EMA平均，Mean Teacher是一个进行了模型权重平均（EMA）的模型                        | ![](https://img2020.cnblogs.com/blog/1351564/202006/1351564-20200605154033235-1551850018.png)                                    |

 



### Π 模型

#### 模型

训练过程的每一个 epoch 中，同一个无标签样本前向传播（forward）**两次**，通过 data augmentation 和 dropout 注入扰动（或者说随机性、噪声），同一样本的两次 forward 会得到不同的 predictions，Π-Model 希望这两个 predictions 尽可能一致，即模型对扰动鲁棒。

![](https://img2020.cnblogs.com/blog/1351564/202006/1351564-20200609091901374-2059403596.png)







### Temporal Ensembling for Semi-Supervised Learning

论文 | https://arxiv.org/abs/1610.02242

改进方向：相较于 Π模型， 训练过程的每一个 epoch 中，同一个无标签样本前向传播（forward）**一次**。那么另一次怎么办呢？

Temporal Ensembling 使用之前 epochs得到的 predictions替代， 具体方法是<mark>使用EMA（指数移动平均）计算之前epochs的Predictions</mark>， 使得forward的次数减少一般， 速度提高一倍

Temporal Ensembling 的 ensembling在哪？通过 EMA 来平均之前 epochs 的模型的输出，这隐式地利用了集成学习的思想。

> 一个问题，利用 EMA 能得到当前 epoch 下模型准确的 prediction 吗？在训练前期，模型经过一个 epoch 训练提升就很大，这个时候很可能就是不准的，即使 EMA 有集成学习的思想；在训练后期，模型效果一个 epoch 提升不明显或者较小，这个时候 EMA 得到的 prediction 和当前 epoch 下的 prediction 应该就相近了。而随训练过程逐渐增大无标签样本权重 w(t) 可以缓解这个问题。

#### 模型

![](https://img2020.cnblogs.com/blog/1351564/202006/1351564-20200609091937752-414637732.png)

个人理解：类似Memory bank的做法， 但是存储之前的结果 数量可能存在差异









### Mean Teacher

#### Mean teachers are better role models: Weight-averaged consistency targets improve semi-supervised deep learning results

参考 | https://zhuanlan.zhihu.com/p/403219187

作者 | [Antti Tarvainen](https://link.zhihu.com/?target=https%3A//arxiv.org/search/cs%3Fsearchtype%3Dauthor%26query%3DTarvainen%252C%2BA),[Harri Valpola](https://link.zhihu.com/?target=https%3A//arxiv.org/search/cs%3Fsearchtype%3Dauthor%26query%3DValpola%252C%2BH)

论文 | https://arxiv.org/pdf/1703.01780

代码 | https://github.com/CuriousAI/mean-teacher

![](https://img2020.cnblogs.com/blog/1351564/202006/1351564-20200605154033235-1551850018.png)

Mean Teacher 则是 Temporal Ensembling 的改进版，Mean Teacher 认为 Temporal Ensembling 对模型的预测 predictions 进行[指数滑动平均（Exponentially Moving Average，EMA）](https://www.cnblogs.com/wuliytTaotao/p/9479958.html)并不好，因为 Temporal Ensembling 每个 epoch 才进行一次 EMA，而如果改成对模型权重进行 EMA 的话，每个 step 就可以进行一次，这样岂不是更好。（在 mini-batch 训练模式中，一个 epoch 有很多 steps，一个 step 理解为模型权重的一次更新。batch size 一定时，数据集越大，一个 epoch 含有的 step 数越多。）

##### 方法

- 使用$\theta_t$表示t时刻的student model parameter, $\theta_t^{\prime}$表示t时刻的teacher model parameter.

- teacher model 的参数更新公式 ： $\theta_t^{\prime}=\alpha \theta_t^{\prime} + (1-\alpha)\theta_t$

- student model 的参数更新为SGD方式， 总损失为$\ell = \ell_s +\lambda \,J(\theta)$

- $\ell_s$为student model的分类损失；$\lambda$为一致性权重；$J(\theta)$ 为一致性损失，作为衡量teacher model与student model对sample $x$ 的prediction的距离（这里采用MSE来衡量，后面有实验尝试用KL-divergence来衡量）:
  
  $J(\theta)= \mathbb{E}_{x,\eta,\eta^{\prime}}[||f(x, \theta^{\prime}, \eta^{\prime}) - f(x, \theta, \eta)||^2]$
  
  这里的不同noise  $\eta$和$\eta^{\prime}$可以通过用不同的input augmentation实现

##### 实验结果

![](https://pic1.zhimg.com/80/v2-470a2d8f52743bb046cc20721d9fc180_720w.jpg)

##### 总结

- temporal ensembling对prediction进行ensemble，但是每个epoch每个sample只被更新一次，效率较低，而且需要存储所有sample的的EMA值，空间开销大。而Mean-Teacher是每个mini-batch的更新都对整个model进行ensemble，直觉上效率更高。
- weighted average的是整个model params，因此不仅是final layer的output被EMA，中间所有的layer都被EMA，因此Mean-Teacher拥有更好的intermediate representation，可以理解为中间的hidden representation更加robust吧
- 前面的两个优点让Mean-Teacher有更好的accuracy
- Mean-Teacher适合large scale数据和online learning

---
