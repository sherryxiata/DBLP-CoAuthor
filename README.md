# 利用关联规则（Apriori和FPGrowth）挖掘DBLP数据集中的合作者

## 目标

挖掘DBLP数据集中，经常一起合作的作者信息。

## 数据集

DBLP：计算机领域英文文献集成数据库。

官网：https://dblp.uni-trier.de/db/

数据下载地址：https://dblp.uni-trier.de/xml/（下载dblp.xml.gz和dblp.dtd）

DBLP数据以xml标签格式存储，dblp.xml.gz是整个xml文件的压缩包，解压后2.53G，随着数据库不断更新还会越来越多；dblp.dtd是格式说明文件。解析的时候和前者放在一起。

## 关联规则
1.参考大佬的代码实现fpgrowth（全部700w条数据）；加入了all_confidence、max_confidence、kulc、cosine、coherence5个有效性评价指标。

传送门：https://github.com/findmyway/DBLP-Coauthor

2.基于mlxtend开源包分别实现Apriori和FPGrowth；取了前10000条数据。

## 文件说明
#### config.py
项目的配置文件

#### getAuthors.py
解析dblp.xml，得到所有文章、书、会议等的作者列表authors.txt

#### encode.py
对authors.txt进行编码，生成authors_encoded.txt（编码后的文件）和authors_index（索引）.txt

#### view_data.py
计算每个author的support,得到每种support下的author数目，可视化，为后面support的选取做准备。

#### FPGrowth.py
用FPGrowth生成关联规则,计算规则有效性指标

#### Apriori.py
用Apriori生成关联规则，取了前10000条。

#### aprioriMlxtend.py
用mlxtend的apriori包实现关联规则挖掘。

因为原始数据量太大，所以取了前10000条。

#### FPGrowthMlxtend.py
用mlxtend的FPGrowth包实现关联规则挖掘。

同上，取了10000条。

----

mlxtend是一个类似sklearn的很简洁的Python科学计算包。

文档：http://rasbt.github.io/mlxtend/user_guide/frequent_patterns/apriori/?spm=a2c4e.10696291.0.0.272f19a4FxMdDj

但它在做关联规则挖掘时，要把数据组织成one-hot编码形式，还是很占空间的。






